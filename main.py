from csv_processor import process_csv
from content_generator import generate_blog_post
from image_generator import generate_and_save_images
from seo_module import generate_seo_recommendations
from docx_creator import create_docx
from html_converter import generate_html_with_gpt, save_html_content
from social_media_content import generate_facebook_posts, save_facebook_posts_to_csv
# from wordpress_integration import post_to_wordpress
from post_to_wordpress import post_to_wordpress



def main():
    data = process_csv("/home/daesilin/scripts/NewAutoBlog/sample.csv")
    
    print(f"Number of rows in CSV: {len(data)}")  # To check the number of rows processed

    for row in data:
        print(f"Processing row: {row}")  # To check each row being processed

        topic = row['topic']
        audience = row['audience']
        tone = row['tone']
        bLength = row['bLength']
        PostDate = row['PostDate']


        blog_post = generate_blog_post(topic, audience, tone, bLength)
        if not blog_post:
            print(f"Failed to generate blog post for topic: {topic}")
            continue

        images = generate_and_save_images([topic])
        
        yoast_seo_data, tags = generate_seo_recommendations(blog_post, audience)
        if not yoast_seo_data:
            print(f"Failed to generate SEO data for topic: {topic}")
            continue

        html_content = generate_html_with_gpt(blog_post)
        if html_content:
            save_html_content(html_content, topic)

        try:
            post_to_wordpress(topic, html_content, yoast_seo_data, tags, PostDate,images)
        except Exception as e:
            print(f"Failed to post to WordPress for topic: {topic}. Error: {e}")
                # Generate Facebook posts
        facebook_posts = generate_facebook_posts(topic, blog_post, tone)
        if facebook_posts:
            save_facebook_posts_to_csv(topic, facebook_posts)
        else:
            print(f"Failed to generate Facebook posts for topic: {topic}")
        
        create_docx(topic, blog_post, images, yoast_seo_data, tags, facebook_posts)


if __name__ == "__main__":
    main()
