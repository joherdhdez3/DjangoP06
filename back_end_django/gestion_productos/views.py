from django.shortcuts import render

# Create your views here.
# gestion_productos/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .productoDAO import ProductoDAO
from .serializers import ProductoCompletoSerializer, ProductoParcialSerializer
from gestion_productos.serializers import ProductoCompletoSerializer, ProductoParcialSerializer
from gestion_productos.exceptions.productoExceptions import (
    DatosInvalidos_400,
    ProductoNoEncontrado_404,
    ConflictoProducto_409,
    ErrorInternoServidor_500,
    ProductoNoAutorizado_401,
    ProductoProhibido_403,
)


class ProductoViewSet(viewsets.ViewSet):
    """
    API para la gestión de Productos.
    """

    @swagger_auto_schema(
        operation_summary="Obtener todos los productos",
        responses={
            200: "Éxito",
            401: "No autorizado",
            403: "Prohibido",
            500: "Error interno del servidor",
        },
    )
    def list(self, request, *args, **kwargs):
        """Devuelve una lista de todos los productos con soporte para paginación, ordenamiento y filtrado."""
        try:
            productos = ProductoDAO.obtener_todos()
            serializer = ProductoCompletoSerializer(productos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ProductoNoAutorizado_401 as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        except ProductoProhibido_403 as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        except ErrorInternoServidor_500 as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Obtener un producto por ID",
        responses={
            200: "Éxito",
            401: "No Autorizado",
            403: "Prohibido",
            404: "Producto no encontrado",
            500: "Error interno del servidor",
        },
    )
    def retrieve(self, request, pk=None):
        """Obtiene los detalles de un producto específico utilizando su ID."""
        try:
            producto = ProductoDAO.obtener_producto_por_id(pk)
            serializer = ProductoCompletoSerializer(producto)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ProductoNoAutorizado_401 as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        except ProductoProhibido_403 as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ErrorInternoServidor_500 as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Crear un nuevo producto",
        request_body=ProductoCompletoSerializer,
        responses={
            201: "Producto creado exitosamente",
            400: "Error en la validación",
            409: "Conflicto (product_key ya registrado)",
            500: "Error interno del servidor",
        },
    )
    def create(self, request):
        """Crea un nuevo producto con la información proporcionada en el cuerpo de la petición."""
        try:
            producto = ProductoDAO.crear_producto(**request.data)
            return Response(
                ProductoCompletoSerializer(producto).data,
                status=status.HTTP_201_CREATED
            )

        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except ConflictoProducto_409 as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

        except ErrorInternoServidor_500 as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Actualizar un producto (completo)",
        request_body=ProductoCompletoSerializer,
        responses={
            200: "Producto actualizado exitosamente",
            400: "Datos inválidos",
            404: "Producto no encontrado",
            409: "Conflicto (product_key ya registrado)",
            500: "Error interno del servidor",
        },
    )
    def update(self, request, pk=None):
        """Actualiza completamente un producto especificado por su ID."""
        try:
            productoDTO = ProductoDAO.actualizar_producto(pk, **request.data)
            return Response(
                ProductoCompletoSerializer(productoDTO).data,
                status=status.HTTP_200_OK
            )

        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ConflictoProducto_409 as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

        except ErrorInternoServidor_500 as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Actualizar un producto (parcialmente)",
        request_body=ProductoParcialSerializer,
        responses={
            200: "Producto actualizado parcialmente",
            400: "Datos inválidos",
            404: "Producto no encontrado",
            409: "Conflicto (product_key ya registrado)",
            500: "Error interno del servidor",
        },
    )
    def partial_update(self, request, pk=None):
        """Actualiza parcialmente un producto especificado por su ID."""
        try:
            productoDTO = ProductoDAO.actualizar_producto_parcial(pk, **request.data)
            return Response(
                ProductoParcialSerializer(productoDTO).data,
                status=status.HTTP_200_OK
            )

        except DatosInvalidos_400 as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ConflictoProducto_409 as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

        except ErrorInternoServidor_500 as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Elimina un producto (borrado lógico).",
        responses={
            200: "Producto eliminado correctamente",
            401: "No autorizado",
            400: "Error en la validación",
            404: "Producto no encontrado",
        },
    )
    def destroy(self, request, pk=None):
        """Marca el producto como eliminado sin borrarlo físicamente."""
        try:
            ProductoDAO.eliminar_producto(pk)
            return Response(
                {"mensaje": "Producto eliminado correctamente"},
                status=status.HTTP_200_OK
            )

        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Restaurar un producto eliminado.",
        responses={
            200: "Producto restaurado exitosamente",
            401: "No autorizado",
            400: "El producto no estaba eliminado",
            404: "Producto no encontrado",
        },
    )
    def restore(self, request, pk=None):
        """Restaura un producto eliminado lógicamente."""
        try:
            ProductoDAO.restaurar_producto(pk)
            return Response(
                {"mensaje": "Producto restaurado correctamente"},
                status=status.HTTP_200_OK
            )

        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="search")
    @swagger_auto_schema(
        operation_summary="Buscar productos por nombre o descripción",
        manual_parameters=[
            openapi.Parameter(
                "q", openapi.IN_QUERY,
                description="Texto a buscar en nombre o descripción",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: ProductoCompletoSerializer(many=True),
            400: "Consulta de búsqueda inválida",
            401: "No autorizado",
            403: "Prohibido",
            404: "No se encontraron productos",
            500: "Error interno del servidor"
        }
    )
    def search(self, request):
        query = request.GET.get("q", "")
        if not query:
            return Response(
                {"error": "Debe proporcionar un parámetro de búsqueda"},
                status=status.HTTP_400_BAD_REQUEST
            )

        productos = ProductoDAO.buscar_productos(query)
        serializer = ProductoCompletoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Actualizar imagen de producto",
        manual_parameters=[
            openapi.Parameter(
                "image_link", openapi.IN_QUERY,
                description="string (URL válida , máximo 200 caracteres)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: "Imagen actualizada exitosamente",
            400: "URL inválida o excede el límite de caracteres",
            404: "Producto no encontrado",
            500: "Error interno del servidor"
        }
    )
    def update_image(self, request, pk=None):
        """Actualiza la URL de la imagen de un producto específico."""
        try:
            img = request.GET.get("image_link", "")
            producto = ProductoDAO.actualizar_img(pk, img)

            data = {
                "codigo": 200,
                "mensaje": "Imagen del producto actualizada exitosamente.",
                "resultado": {
                    "id": str(producto.id),
                    "image_link": producto.image_link,
                    "modified_at": producto.modified_at.isoformat()
                }
            }
            return Response(data, status=status.HTTP_200_OK)

        except ProductoNoEncontrado_404 as e:
            data = {"codigo": 404, "mensaje": "Producto no encontrado.", "resultado": "null"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        except ValidationError:
            data = {
                "codigo": 400,
                "mensaje": "La URL de la imagen no es válida o excede el límite de caracteres.",
                "resultado": "null"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            data = {
                "codigo": 500,
                "mensaje": "Error interno del servidor al actualizar la imagen.",
                "resultado": "null"
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Desactivar un producto",
        responses={
            200: "Producto desactivado exitosamente",
            401: "No autorizado",
            400: "El producto ya estaba desactivado",
            403: "Prohibido",
            404: "Producto no encontrado",
            500: "Error interno del servidor"
        }
    )
    def deactivate(self, request, pk=None):
        """Desactiva un producto estableciendo el campo status en false."""
        try:
            producto = ProductoDAO.desactivar_producto(pk)
            data = {
                "codigo": 200,
                "mensaje": "Producto desactivado exitosamente.",
                "resultado": {
                    "id": str(producto.id),
                    "status": producto.status,
                    "modified_at": producto.modified_at.isoformat()
                }
            }
            return Response(data, status=status.HTTP_200_OK)

        except ProductoNoEncontrado_404 as e:
            return Response({"codigo": 404, "mensaje": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({"codigo": 400, "mensaje": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"codigo": 500, "mensaje": "Error interno del servidor", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=["patch"])
    @swagger_auto_schema(
        operation_summary="Activar un producto",
        responses={
            200: "Producto activado correctamente",
            401: "No autorizado",
            400: "El producto ya estaba activado",
            404: "Producto no encontrado"
        }
    )
    def activate(self, request, pk=None):
        """Activa un producto estableciendo el campo status en true."""
        try:
            ProductoDAO.activar_producto(pk)
            return Response({"mensaje": "Producto activado correctamente"}, status=status.HTTP_200_OK)

        except ProductoNoEncontrado_404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# Archivo: gestion_productos/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from gestion_productos.models import Productos
from gestion_productos.serializers import ProductoCompletoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API para la gestión de Productos.
    Solo los usuarios autenticados pueden acceder a estos endpoints.
    """
    queryset = Productos.objects.all()
    serializer_class = ProductoCompletoSerializer
    permission_classes = [IsAuthenticated]       