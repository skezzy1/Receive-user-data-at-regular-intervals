import requests
import logging
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from core.config import get_settings

from users.models import UserModel, AddressModel, GeoModel
from company.models import CompanyModel
from posts.models import PostModel
from comments.models import CommentsModel

logger = logging.getLogger(__name__)


class BaseImporter(ABC):
    def __init__(self, session: Session):
        self.session = session
        self.base_url = get_settings().API_BASE_URL

    def _fetch_from_api(self, endpoint: str) -> list[dict]:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch data from {url}: {e}")
            raise

    @abstractmethod
    def run(self):
        pass


class UserImporter(BaseImporter):
    def _get_or_create_geo(self, lat: float, lng: float) -> GeoModel:
        geo = self.session.query(GeoModel).filter_by(lat=lat, lng=lng).first()
        if not geo:
            geo = GeoModel(lat=lat, lng=lng)
            self.session.add(geo)
            self.session.flush()
        return geo

    def _get_or_create_address(self, data: dict, geo: GeoModel) -> AddressModel:
        addr = self.session.query(AddressModel).filter_by(zipcode=data['zipcode']).first()
        if not addr:
            addr = AddressModel(
                street=data['street'],
                suite=data['suite'],
                city=data['city'],
                zipcode=data['zipcode'],
                geo=geo
            )
            self.session.add(addr)
            self.session.flush()
        return addr

    def _get_or_create_company(self, data: dict) -> CompanyModel:
        company = self.session.query(CompanyModel).filter_by(name=data['name']).first()
        if not company:
            company = CompanyModel(
                name=data['name'],
                catchPhrase=data['catchPhrase'],
                bs=data['bs']
            )
            self.session.add(company)
            self.session.flush()
        return company

    def run(self):
        logger.info("Running UserImporter...")
        users_data = self._fetch_from_api("users")

        count = 0
        for u in users_data:
            geo = self._get_or_create_geo(float(u['address']['geo']['lat']), float(u['address']['geo']['lng']))
            address = self._get_or_create_address(u['address'], geo)
            company = self._get_or_create_company(u['company'])

            user = self.session.query(UserModel).filter_by(id=u['id']).first()
            if not user:
                user = UserModel(id=u['id'])

            user.name = u['name']
            user.username = u['username']
            user.email = u['email']
            user.password = "default_pass"
            user.phone = u['phone']
            user.website = u['website']
            user.address = address
            user.company = company

            self.session.add(user)
            count += 1

        self.session.commit()
        logger.info(f"UserImporter finished. Processed {count} users.")


class PostImporter(BaseImporter):

    def _get_valid_user_ids(self) -> set[int]:
        return {u.id for u in self.session.query(UserModel.id).all()}

    def run(self):
        logger.info("Running PostImporter...")
        posts_data = self._fetch_from_api("posts")
        valid_users = self._get_valid_user_ids()

        count = 0
        for p in posts_data:
            if p['userId'] not in valid_users:
                continue

            post = self.session.query(PostModel).filter_by(id=p['id']).first()
            if not post:
                post = PostModel(id=p['id'])

            post.title = p['title']
            post.body = p['body']

            post.user_id = p['userId']

            self.session.add(post)
            count += 1

        self.session.commit()
        logger.info(f"PostImporter finished. Processed {count} posts.")


class CommentImporter(BaseImporter):
    def _get_valid_post_ids(self) -> set[int]:
        return {p.id for p in self.session.query(PostModel.id).all()}

    def run(self):
        logger.info("Running CommentImporter...")
        comments_data = self._fetch_from_api("comments")
        valid_posts = self._get_valid_post_ids()

        count = 0
        for c in comments_data:
            if c['postId'] not in valid_posts:
                continue

            comment = self.session.query(CommentsModel).filter_by(id=c['id']).first()
            if not comment:
                comment = CommentsModel(id=c['id'])

            comment.name = c['name']
            comment.email = c['email']
            comment.body = c['body']

            comment.post_id = c['postId']

            self.session.add(comment)
            count += 1

        self.session.commit()
        logger.info(f"CommentImporter finished. Processed {count} comments.")
