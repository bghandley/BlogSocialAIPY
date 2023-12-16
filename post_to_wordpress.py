import os
from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost, xmlrpc_client
from wordpress_xmlrpc.methods.posts import NewPost
from datetime import datetime
from wordpress_xmlrpc.methods.media import UploadFile


def upload_image_to_wordpress(image_path, wp_client):
    """
    Uploads an image to WordPress and returns its URL.

    :param image_path: The path to the image file.
    :param wp_client: The WordPress XML-RPC client.
    :return: URL of the uploaded image.
    """
    with open(image_path, 'rb') as img:
        data = {
            'name': os.path.basename(image_path),
            'type': 'image/png',  # or 'image/jpeg' etc, based on your image type
            'bits': xmlrpc_client.Binary(img.read()),
        }

    response = wp_client.call(UploadFile(data))
    return response['url']


def post_to_wordpress(topic, html_content, yoast_seo_data, tags, PostDate, images):
    """
    Post content to a WordPress site using XML-RPC.

    :param new_title: Title of the blog post.
    :param html_formatted_blog_post: HTML content of the blog post.
    :param yoast_seo_data: Dictionary containing Yoast SEO data.
    :param tags: List of tags for the post.
    :param post_date: Optional date to schedule the post.
    """
    wp_url = "https://website.com/xmlrpc.php"
    wp_username = os.environ.get("WP_USERNAME")
    wp_password = os.environ.get("WP_PASSWORD")

    wp_client = Client(wp_url, wp_username, wp_password)

    # Handle image uploads and get their URLs
    image_urls = [upload_image_to_wordpress(image_path, wp_client) for image_path in images]

    # Modify the post content to include images
    image_html = ''.join([f"<img src='{url}' alt='Image related to {topic}' /><br/>" for url in image_urls])
    modified_html_content = image_html + html_content

    # Create a new WordPress post
    post = WordPressPost()
    post.title = yoast_seo_data['seo_title']
    post.content = modified_html_content
    post.terms_names = {'post_tag': tags}

    # Add the Yoast SEO data as custom fields
    post.custom_fields = [
        {'key': '_yoast_wpseo_focuskw', 'value': yoast_seo_data['focus_keyphrase']},
        {'key': '_yoast_wpseo_title', 'value': yoast_seo_data['seo_title']},
        {'key': '_yoast_wpseo_metadesc', 'value': yoast_seo_data['meta_description']}
    ]

    # Set the post slug
    post.slug = yoast_seo_data['slug']
    
    # Set the post date or status
    if PostDate:
        try:
            # Attempt to parse the date in 'YYYY-MM-DD HH:MM:SS' format first
            post_date = datetime.strptime(PostDate, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If the above fails, try 'MM/DD/YYYY' format
            post_date = datetime.strptime(PostDate, "%m/%d/%Y")
        
        post.date = post_date

    # Upload the post to WordPress
    post_id = wp_client.call(NewPost(post))
    print(f"Post uploaded to WordPress with ID: {post_id}")

# Example usage
# post_to_wordpress("Your Post Title", "<p>Your HTML content</p>", yoast_seo_data, ["tag1", "tag2"], "2023-11-10 10:00:00")
