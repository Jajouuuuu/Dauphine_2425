from ariadne import QueryType, MutationType, make_executable_schema
from domain.port.review_repository import ReviewRepository

query = QueryType()
mutation = MutationType()

def get_graphql_schema(repo: ReviewRepository):

    @query.field("allUsers")
    def resolve_all_users(_, info):
        return repo.get_all_users()

    @query.field("myFriends")
    def resolve_my_friends(_, info, username):
        return repo.get_user_friends(username)

    @query.field("allContent")
    def resolve_all_content(_, info):
        return repo.get_all_content()

    @query.field("friendReviews")
    def resolve_friend_reviews(_, info, username):
        return repo.get_friend_reviews(username)

    @query.field("myReviews")
    def resolve_my_reviews(_, info, username):
        return repo.get_user_reviews(username)

    @mutation.field("addFriend")
    def resolve_add_friend(_, info, username, friendName):
        return repo.add_friend(username, friendName)

    @mutation.field("removeFriend")
    def resolve_remove_friend(_, info, username, friendName):
        return repo.remove_friend(username, friendName)

    @mutation.field("createReview")
    def resolve_create_review(_, info, username, contentTitle, rating, comment):
        return repo.create_review(username, contentTitle, rating, comment)

    @mutation.field("deleteReview")
    def resolve_delete_review(_, info, reviewId):
        return repo.delete_review(reviewId)

    # Charger le schéma depuis le fichier séparé
    from .schema import type_defs
    return make_executable_schema(type_defs, query, mutation)