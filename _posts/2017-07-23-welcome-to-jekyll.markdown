---
layout: post
title:  "Installing jekyll on debian 9"
date:   2017-07-23 14:20:34 +0200
categories: jekyll update debian static blogging
---

After going through the documentation to deploy a
[Zinnia Blog][zinnia-django-blog]
on a remote debian VPS, I preferred to go the easy way by deploying
a static blog based on simple git-hooks for automatic publication and using Jekyll.

Why Jekyll ? It is the standard off-the-mill static website generator, and it seems
to have a very broad community of users.

I was not very familiar with the ruby environment, but running `gem install jekyll`
so far has not been hard. I decided to install all the required
gem locally to keep my system as clean as possible.

The [deployment section][jekyll-docs-deployment]
gives a git post-receive hook to build
your website after each push on the git remote repository. I had to
put an additional file at the top of this shell script to put the
user-wide installation of jekyll in the path.

To be able to serve the blog, I added a really simple nginx configuration
that does the job quite easily.

{% highlight nginx %}
  server {
    location / {
     root /var/www/jekyll-blog;
    }
    server_name david-kremer.fr;
    access_log /var/log/nginx/jekyll-blog.log;
}
{% endhighlight %}

In the end, it was more rewarding when you want to publish fast, instead of having to
run a database engine and all the stuff that goes along (automatic deployment,
WSGI job, database maintenance, etc). All this work is quite huge and I don't think
anybody would benefit from maintaining such a stack just for the sake of a single
user's blog.

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-docs-deployment]: https://jekyllrb.com/docs/deployment-methods/
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
[zinnia-django-blog]: https://github.com/Fantomas42/django-blog-zinnia
