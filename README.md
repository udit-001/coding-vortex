# Coding Vortex

## Overview
A Blog CMS made using Django that allows you to create posts by using the Django Admin with the help of a WYSIWYG editor, comes with a tagging system, integrated Disqus comments system, contact form to allow visitors to send queries to the authors. 

The Blog also has a REST API which can be used to create client on multiple platforms such as Android, iOS etc. The API comes with search, sorting and filtering abilities.

## Features
- 🤖 **API** : The Blog comes with an API which allows developers to built client side applications for different platforms such as Android and iOS etc.
- 🗂️ **Categories** : Posts can be grouped together with the help of categories and be used to display similar blog posts to the users.
- 💬 **Disqus Comments** : Each post will have a comments section attached at the end of the article so that visitors can have a discussion relating to the content of the article.
- 📄 **Pagination** : Every results page including the homepage of the blog and API will come along with pagination features so as to reduce load on the client side.
- 🕘 **Read time estimation** : Each article's reading time will be estimated and displayed to the user in a similar manner to the popular blogging site Medium.
- 📰 **Related Posts** : Similar posts will be displayed to the user at the end of each article.
- 🔎 **Search** : Allows user to search through the posts available on the blog.
- 🔗 **Share buttons** : Presents users with the sharing buttons on each page so they can easily share an article with someone. 
- 🔍 **SEO Settings** : It allows authors to control how the articles will be displayed into the search. 
- 🏷️ **Tags** : Posts can have multiple tags which can be used to find similar posts. 
- 👨‍💻 **Code Syntax Highlighting** : The blog displays text, especially source code, in different colors and fonts according to the category of terms.

## Technical Details

### Frontend
- [Prism](https://prismjs.com/) :  Adds the code syntax highlighting functionality.
- [Disqus](https://disqus.com/) : Adds the disqus comment box unique for each post.

### Backend
- [django-rest-framework](https://www.django-rest-framework.org/) : Django REST framework is a powerful and flexible toolkit for building Web APIs.

- [django-taggit](https://github.com/jazzband/django-taggit) : Allows us to add tagging system to our existing models.
- [django-taggit-serializer](https://github.com/glemmaPaul/django-taggit-serializer) : Adds functionality for using taggit with django-rest-framework.
- [django-taggit-selectize](https://github.com/chhantyal/taggit-selectize) : Adds the autocomplete functionality in django admin for tags fields.
- [django-recaptcha](https://github.com/praekelt/django-recaptcha) : Allows us to add Google Recaptcha as fields to our forms for spam protection.
- [django-cors-headers](https://github.com/adamchainz/django-cors-headers) : Lets us handle the server headers required for Cross-Origin Resource Sharing (CORS)
- [django-tinymce4-lite](https://github.com/romanvm/django-tinymce4-lite) : TinyMCE 4 editor is WYSIWYG editor that allows us to edit rich content in django admin.
- [django-filter](https://django-filter.readthedocs.io/en/master/) : Allows users to filter down a queryset based on a model’s fields
- [django-environ](https://github.com/joke2k/django-environ) : Used to configure secret keys, API keys through environment variables.
- [django-cloudinary-storage](https://github.com/klis87/django-cloudinary-storage) : Lets you serve static files and media files through cloudinary CDN.
