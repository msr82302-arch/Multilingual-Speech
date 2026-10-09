import logging
import time
from api.common.pipeline import SpeechToSpeechPipeline
#rom api.common.mongo_service import save_translation

logger = logging.getLogger(__name__)


class ProcessService:


 def run(self,validated_data, user):
    start_time = time.time()

    text = validated_data.get("text")
    audio_file = validated_data.get("audio")
    target_lang = validated_data["target_lang"]
    source_lang = validated_data.get("source_lang") or None

    pipeline = SpeechToSpeechPipeline()

    logger.info(f"Pipeline started for user {user.id}")

    result = pipeline.run(
        text=text,
        audio_file=audio_file,
        source_language=source_lang,
        target_language=target_lang,
    )

    translated_text = result.get("translated_text")

    

    end_time = time.time()
    execution_time = round(end_time - start_time, 3)

    logger.info(
        f"Pipeline completed for user {user.id} "
        f"in {execution_time} seconds"
    )

    return result

'''
    def execute(self, validated_data, user):
        
        start_time = time.time()

        text = validated_data.get("text")
        audio_file = validated_data.get("audio")
        target_lang = validated_data["target_lang"]
        source_lang = validated_data.get("source_lang") or None

        pipeline = SpeechToSpeechPipeline()
      

    logger.info(f"Pipeline started for user {user.id}")

    result = pipeline.run(
        text=text,
        audio_file=audio_file,
        source_language=source_lang,
        target_language=target_lang,
    )

    translated_text = result.get("translated_text")

    try:
        save_translation(
            user_id=user.id,
            original_text=text,
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=target_lang,
        )
    except Exception as db_error:
        logger.warning(f"Mongo save failed: {str(db_error)}")

    end_time = time.time()
    execution_time = round(end_time - start_time, 3)

    logger.info(
        f"Pipeline completed for user {user.id} "
        f"in {execution_time} seconds"
    )

    return result


    

    def execute(self, validated_data, user):

        text = validated_data.get("text")
        audio_file = validated_data.get("audio")
        target_lang = validated_data["target_lang"]
        source_lang = validated_data.get("source_lang") or None

        pipeline = SpeechToSpeechPipeline()

        #ger.info(f"Pipeline started for user {user.id}")
        logger.info("Pipeline started", extra={"user_id": user.id})

        result = pipeline.run(
            text=text,
            audio_file=audio_file,
            source_language=source_lang,
            target_language=target_lang,
        )

        translated_text = result.get("translated_text")

        # Optional DB save (safe mode)
        try:
            save_translation(
                user_id=user.id,
                original_text=text,
                translated_text=translated_text,
                source_lang=source_lang,
                target_lang=target_lang,
            )
        except Exception as db_error:
            logger.warning(f"Mongo save failed: {str(db_error)}")

        logger.info(f"Pipeline completed for user {user.id}")

        return result'''