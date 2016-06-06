from django.conf.urls import url, include
from api import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'units', views.UnitViewSet)
router.register(r'notes', views.NoteViewSet)
router.register(r'steps', views.StepViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'recipeingredients', views.RecipeIngredientViewSet)
router.register(r'recipedatas', views.RecipeDataViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
