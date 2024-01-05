from pydantic import BaseModel
from typing import Dict, List

from business.db.media_service import MediaDBService, MediaThumbnail, MediaObjectEnum
from business.db.user_service import UserDBService
from business.db.insights_service import InsightEngineService
from .models import Page, MediaView, MediaViewInsightCollection
from project_shkedia_models.insights import InsightObjectEnum, Insight
from project_shkedia_models.jobs import InsightJobStatus, InsightJob
from business.encryption.service import DecryptService
from business.image_processing.service import ImageProcessingService

class MediaViewService:
    def __init__(self,
                 media_db_service: MediaDBService,
                 user_db_service: UserDBService,
                 decrypt_service: DecryptService,
                 engine_service: InsightEngineService) -> None:
        
        self.media_db_service = media_db_service
        self.user_db_service = user_db_service
        self.decrypt_service = decrypt_service
        self.engine_service=engine_service

    def get_media_content(self, token, media_id, user_id) -> MediaView:
        # media_content = [media for media in self.cache_object[user_id].list_of_images if media.media_id==media_id][-1]
        # if media_content is None:
        #     raise Exception("Could find media")
        media = self.media_db_service.search_media(token=token,media_id=media_id,response_type=MediaObjectEnum.MediaThumbnail)
        media = self.__decrypt_single_media(MediaThumbnail(**media.results[0]))
        media.user = self.user_db_service.search_user(token, search_field="user_id", search_value=media.owner_id)
        media.device = self.user_db_service.get_device(token, device_id=media.device_id)
        return media
    
    def __group_data_by_engine__(self, insights_list: List[Insight], jobs_list: List[InsightJob]) -> Dict[str,Dict[str,List[Insight]]]:
        collector = MediaViewInsightCollection(insights_list=insights_list,jobs_list=jobs_list)
        temp_dict = {}
        for _, insights_list in collector.group_insights.items():
            engine_id = insights_list[0].insight_engine_id
            engine_name = self.engine_service.get_engine_name_by_id(engine_id)
            insight_name = insights_list[0].name
            if not engine_id in temp_dict:
                temp_dict[engine_name] = {}
            temp_dict[engine_name][insight_name] = insights_list
        return temp_dict

    def get_media_insights(self, token, media_id) -> Dict[str,Dict[str,List[Insight]]]:
        insights_list = self.media_db_service.search_insights(token,media_id=media_id,response_type=InsightObjectEnum.Insight)
        jobs_list = self.media_db_service.search_jobs(token, media_id=media_id)
        jobs_list = [job_item for job_item in jobs_list if job_item.status != InsightJobStatus.DONE]
        return self.__group_data_by_engine__(insights_list=insights_list,jobs_list=jobs_list)
    
    def __decrypt_single_media(self, media: MediaThumbnail) -> MediaView:
        image = self.decrypt_service.decrypt(media.media_key,{"image": media.media_thumbnail})
        image = ImageProcessingService.get_image_base64(image["image"])
        return MediaView(thumbnail=image,**media.model_dump())