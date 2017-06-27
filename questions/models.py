# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import markdown

class Activity(models.Model):
    """
    所有的投票,关注等行为的数据表格,包含了这个行为的用户,以及投票的答案id,关注问题的id
    """
    FAVORITE = "F"
    LIKE = "L"
    UP_VOTE = "U"
    DOWN_VOTE = "D"
    ACTIVITY_TYPES = (
        (FAVORITE, "Favorite"),
        (LIKE, "Like"),
        (UP_VOTE, "Up Vote"),
        (DOWN_VOTE, "Down vote")
    )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    question = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
    
    def __unicode__(self):
        return self.activity_type

class Tag(models.Model):
    """
    问题的标签.
    """
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __unicode__(self):
        return self.name

class Question(models.Model):
    """
    问题的数据库表格.
    """
    # 问题只能有一个user,一对多的情况.
    user = models.ForeignKey(User)
    tag = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    # 关注数.
    favorites = models.IntegerField(default=0)
    # 问题答案是否被采纳.
    has_accepted_answer = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        # 排序按照更新时间
        ordering = ("-update_date",)
    
    def __unicode__(self):
        return self.title

    def get_description_preview(self):
        if len(self.description) > 255:
            return u"{0}......".format(self.description[:255])
        else:
            return self.description
            
    def get_description_preview_as_markdown(self):
        """
        返回问题的描述,如果是markdown格式的也可以正常显示.
        """
        return markdown.markdown(self.get_description_preview(), safe_mode="escape")

    def get_favoriters(self):
        """
        返回关注该问题的用户列表.
        """
        favorites = Activity.objects.filter(activity_type=Activity.FAVORITE, question=self.pk)
        favoriters = []
        for favorite in favorites:
            favoriters.append(favorite.user)
        return favoriters

    def get_answers(self):
        """
        返回该问题下面所有的答案实例.
        """
        return Answer.objects.filter(question=self)

    def calculate_favorite(self):
        """
        计算问题的关注数量.
        """
        favorites = Activity.objects.filter(activity_type=Activity.FAVORITE, question=self.pk).count()
        self.favorites = favorites
        self.save(update_fields=["favorites"])
        return self.favorites

    @staticmethod
    def get_unanswered():
        """
        返回未采纳的问题列表.
        """
        return Question.objects.filter(has_accepted_answer=False)

    @staticmethod
    def get_answered():
        """
        返回采纳的问题列表.
        """
        return Question.objects.filter(has_accepted_answer=True)

class Answer(models.Model):
    """
    回答问题的数据库表格.
    """
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    # 答案内容.
    answer_content = models.TextField(max_length=3000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    # 答案认同数.
    votes = models.IntegerField(default=0)
    # 该答案是否被接受. 
    is_accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        # 先安装是否被接受排序,再安装认同数,最后按照创建时间.
        ordering = ("-is_accepted", "-votes", "create_date")
    
    def __unicode__(self):
        return self.answer_content

    def accept(self):
        """
        设置该答案被接受.
        """
        # 获取到该问题下的所有答案.
        answers = Answer.objects.filter(question=self.question)
        for answer in answers:
            # 将所有的答案设置为没有被接受.
            answer.is_accepted = False
            answer.save(update_fields=["is_accepted"])
        self.is_accepted = True
        self.save(update_fields=["is_accepted"])
        # 将该答案的问题设置为已解决.
        self.question.has_accepted_answer = True
        self.question.save()

    def calculate_votes(self):
        """
        计算投票,投票为赞成票减去反对票.
        最后返回投票数.
        """
        up_votes_count = Activity.objects.filter(activity_type=Activity.UP_VOTE, answer=self.pk).count()
        down_votes_count = Activity.objects.filter(activity_type=Activity.DOWN_VOTE, answer=self.pk).count()
        self.votes = up_votes_count - down_votes_count
        self.save(update_fields=["votes"])
        return self.votes
        
    def get_up_voters(self):
        """
        返回给这个问题投支持票的用户列表.
        """
        votes = Activity.objects.filter(activity_type=Activity.UP_VOTE, answer=self.pk)
        voters = []
        for vote in votes:
            voters.append(vote.user)
        return voters

    def get_down_voters(self):
        votes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE, answer=self.pk)
        voters = []
        for vote in votes:
            voters.append(vote.user)
        return voters

    def get_answercontent_as_markdown(self):
        """
        返回回答内容markdown.
        """
        return markdown.markdown(self.answer_content, safe_mode="escape")

class Notification(models.Model):
    _FAVORITED_TEMPLATE = u'<a href="/{0}/">{1}</a> favorited your question: <a href="/questions/{2}/">{3}</a>'
    _ANSWERED_TEMPLATE = u'<a href="/{0}/">{1}</a> answered your question: <a href="/questions/{2}/">{3}</a>'
    _ACCEPTED_ANSWER_TEMPLATE = u'<a href="/{0}/">{1}</a> accepted your answer: <a href="/questions/{2}/">{3}</a>'

    FAVORITED = "F"
    LIKED = "L"
    ANSWERED = "A"
    ACCEPTED_ANSWER = "W"
    NOTIFICATION_TYPES = (
        (LIKED, "liked"),
        (FAVORITED, "Favorited"),
        (ANSWERED, "Answered"),
        (ACCEPTED_ANSWER, "Accepted_Answer")
    )

    from_user = models.ForeignKey(User, related_name="+")
    to_user = models.ForeignKey(User, related_name="+")
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, blank=True)
    answer = models.ForeignKey(Answer, null=True, blank=True)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-date"]

    def __unicode__(self):

        # '<a href="/{0}/">{1}</a> answered your question: <a href="/questions/{2}/">{3}</a>'
        if self.notification_type == self.ANSWERED:
            return self._ANSWERED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.username),
                self.question.pk,
                escape(self.get_summary(self.answer.answer_content))
            )   
        else:
            return "出错啦！"
    
    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return u"{0}......".format(value[:summary_size])
        else:
            return value
