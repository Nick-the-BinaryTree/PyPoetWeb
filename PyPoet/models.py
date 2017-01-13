from django.db import models

# Create your models here.
class Prompt(models.Model):
    url_text = models.CharField(max_length=200)
    start_index_text = models.CharField(max_length=200)
    total_lines_text = models.CharField(max_length=200)
    target_sentence_length_text = models.CharField(max_length=200)
    sentence_length_threshold = models.CharField(max_length=200)
    result_text = models.TextField()

    def __str__(self):
        return self.prompt_text