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

    # @action(detail=False, methods=['post'], url_path='submit_answers')
    # def submit_answers(self, request):
    #
    #     user_answers_data = request.data  # This will be the list of user answers
    #
    #     # Check if the received data is a list
    #     if not isinstance(user_answers_data, list):
    #         return Response({"error": "Expected a list of answers."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     total_score = 0
    #     total_questions = len(user_answers_data)
    #
    #     for answer_data in user_answers_data:
    #         question_id = answer_data.get('question_id')
    #         answer_text = answer_data.get('answer')
    #
    #         if not question_id or not answer_text:
    #             return Response({"error": "Missing question_id or answer."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #         # Retrieve the question from the database
    #         try:
    #             question = Question.objects.get(id=question_id)
    #         except Question.DoesNotExist:
    #             return Response({"error": f"Question with id {question_id} does not exist."},
    #                             status=status.HTTP_400_BAD_REQUEST)
    #
    #         # Check if the answer is correct
    #         correct_answer = question.correct_answer
    #         if answer_text.lower() == correct_answer.lower():
    #             total_score += 1
    #
    #         # Save the user's answer
    #         user_answer = UserAnswer(user=request.user, question=question, answer=answer_text)
    #         user_answer.save()
    #
    #     # Return the score and a success message
    #     return Response({
    #         "message": "Answers submitted successfully.",
    #         "score": total_score,
    #         "total_questions": total_questions
    #     }, status=status.HTTP_201_CREATED)