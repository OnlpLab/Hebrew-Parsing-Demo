from django.db import models

# Create your models here.

class DepCategory(models.Model):
    title = models.CharField(max_length=40)
    discipline_choices = (('UDH', "Hebrew with UD"), ('YAPH', "Hebrew with old dependencies"))
    discipline = models.CharField(max_length=4, choices=discipline_choices, default='UDH')
    description = models.TextField()
    example_sentence = models.CharField(max_length=200)
    example = models.TextField()
    structural_category_choices = (('null', " "), ('nominals', "Nominals"), ('clauses', "Clauses"), ('modifiers', "Modifier words"), ('function', "Function Words"))
    structural_category = models.CharField(max_length=50, choices=structural_category_choices, default="null",
                                           help_text="Choose the structural category of the dependent")
    functional_category_choices = (('null', " "), ('core', "Core arguments"), ('noncore', "Non-core dependents"), ('nomdep', "Nominal dependents"))
    functional_category = models.CharField(max_length=50, choices=functional_category_choices, default="null",
                                           help_text="Choose the functional category of the dependent in relation to the head")
    statistics = models.IntegerField(help_text="how many occurrences in treebank?", default=0)
    is_language_specific = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)

class PosCategory(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    example_sentence = models.CharField(max_length=200)
    example = models.TextField()

    def __str__(self):
        return self.title

