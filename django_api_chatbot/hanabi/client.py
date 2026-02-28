# from django.conf import settings
# from sambanova import SambaNova


# class HanabiClient:
#     def __init__(self):
#         self.client = SambaNova(
#             api_key=settings.SAMBANOVA_API_KEY
#         )

#     def get_response(self, user_message):
#         completion = self.client.chat.completions.create(
#             model="Llama-4-Maverick-17B-128E-Instruct",
#             messages=[
#                 {"role": "system", "content": "You are a helpful coding assistant."},
#                 {"role": "user", "content": user_message}
#             ]
#         )
#         return completion.choices[0].message.content