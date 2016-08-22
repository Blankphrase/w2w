from django.db import models



class MoviePopularQuery(models.Model):
    page = models.Integer()
    timestamp = models.DateTime()

    class Meta:
        unique_together = ("page",)

    def __str__(self):
        return "{page}/{date}".format(self.page, self.timestamp)


class Movie:
    title = models.TextField()


# from django.db import models
# from django.core.urlresolvers import reverse

# class Item(models.Model):
#     text = models.TextField(default="")
#     list = models.ForeignKey("List", related_name = "items", default = None)

#     class Meta:
#         ordering = ("id",)
#         unique_together = ("list", "text")

#     def __str__(self):
#         return self.text

# class List(models.Model):
    
#     def get_absolute_url(self):
#         return reverse("lists:view_list", args=[self.id])
