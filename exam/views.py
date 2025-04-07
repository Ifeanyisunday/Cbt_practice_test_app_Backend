import random
import requests
from djoser.views import UserViewSet
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from exam.models import Question
from exam.category import categories
from rest_framework.decorators import action
from exam.serializer import QuestionSerializer, CustomUserSerializer




# class CustomUserViewSet(UserViewSet):
#     serializer_class = CustomUserSerializer

class QuestionViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get'], url_path='questions/(?P<amount>\d+)/(?P<category>[^/.]+)')
    def list_with_params(self, request, amount, category):
        user_amount = amount
        user_category = category
        category_ID = 0
        exam_categories = categories

        for category in exam_categories:
            if user_category == category.get("name"):
                category_ID = category.get("id")


        external_api_url = f"https://opentdb.com/api.php?amount={user_amount}&category={category_ID}&type=multiple"
        response = requests.get(external_api_url)

        if response.status_code == 200:
            data = response.json()
            Question.objects.all().delete()
            new_result = []
            for question in data.get("results", []):
                question_text = question.get("question")
                correct_answer = question.get("correct_answer")
                options = question.get("incorrect_answers", []) + [question.get("correct_answer")]
                random.shuffle(options)
                Question.objects.create(
                    question_text=question_text,
                    options=options,
                    correct_answer=correct_answer
                )

            return Response({"message": "Questions Generated successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Error fetching Api"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='get_questions')
    def get_questions(self, request):
        # Fetch all stored questions from the database
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

