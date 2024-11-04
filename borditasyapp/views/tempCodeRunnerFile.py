# class UserLogIn(ObtainAuthToken):
#     def getUserTokens(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token = Token.objects.get(user=user)
#         return Response({
#             'token': token.key,
#             'id': user.pk,
#             'username': user.username
#         })