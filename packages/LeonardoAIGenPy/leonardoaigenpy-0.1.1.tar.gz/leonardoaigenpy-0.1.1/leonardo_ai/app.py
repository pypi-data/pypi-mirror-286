from leonardo_ai import LeonardoAI, LeonardoAIError


def main():
    api_key = "501cd296-31ae-4f7f-b50a-3736218826b7"
    leonardo = LeonardoAI(api_key=api_key)

    image_id = "938ede54-f78f-48bc-be55-8b5d3612cedf"  # The image ID you provided

    try:
        print("Creating motion generation...")
        motion_result = leonardo.create_motion_generation(image_id=image_id)
        print("Motion Generation Result:", motion_result)

        motion_generation_id = motion_result['motionSvdGenerationJob']['generationId']
        print(f"Motion Generation ID: {motion_generation_id}")

        print("Retrieving the motion generation URL...")
        motion_url = leonardo.get_motion_image_url(motion_generation_id)
        print(f"Motion Image URL: {motion_url}")
    except LeonardoAIError as e:
        print(f"LeonardoAIError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
