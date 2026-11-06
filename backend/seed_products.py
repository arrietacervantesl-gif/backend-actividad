
from main import app
from app.models import db, Producto, Categoria

def cargar_productos():

    with app.app_context():

        # Crear las tablas si todavía no existen
        db.create_all()

        # Categorías de ejemplo
        categorias = [
            {
                "nombre": "Tecnología",
                "descripcion": "Productos tecnológicos"
            },
            {
                "nombre": "Ropa",
                "descripcion": "Prendas de vestir"
            },
            {
                "nombre": "Accesorios",
                "descripcion": "Accesorios personales"
            },
            {
                "nombre": "Hogar",
                "descripcion": "Productos para el hogar"
            }
        ]

        # Crear categorías sin duplicarlas
        for item in categorias:

            categoria = db.session.execute(
                db.select(Categoria).where(
                    Categoria.categoria_nombre == item["nombre"]
                )
            ).scalar_one_or_none()

            if not categoria:
                categoria = Categoria(
                    categoria_nombre=item["nombre"],
                    descripcion=item["descripcion"]
                )
                db.session.add(categoria)

        db.session.flush()

        # Productos de ejemplo
        productos = [
            {
                "nombre": "Audífonos Bluetooth",
                "descripcion": "Audífonos inalámbricos con sonido de alta calidad",
                "precio": 85000,
                "stock_min": 10,
                "categoria": "Tecnología"
            },
            {
                "nombre": "Reloj Inteligente",
                "descripcion": "Smartwatch moderno con pantalla digital",
                "precio": 150000,
                "stock_min": 5,
                "categoria": "Tecnología"
            },
            {
                "nombre": "Teclado Gamer",
                "descripcion": "Teclado mecánico para videojuegos",
                "precio": 120000,
                "stock_min": 8,
                "categoria": "Tecnología"
            },
            {
                "nombre": "Camiseta Deportiva",
                "descripcion": "Camiseta cómoda para hacer deporte",
                "precio": 45000,
                "stock_min": 15,
                "categoria": "Ropa"
            },
            {
                "nombre": "Chaqueta Casual",
                "descripcion": "Chaqueta moderna para uso diario",
                "precio": 110000,
                "stock_min": 7,
                "categoria": "Ropa"
            },
            {
                "nombre": "Gorra Urbana",
                "descripcion": "Gorra ajustable de estilo urbano",
                "precio": 35000,
                "stock_min": 12,
                "categoria": "Accesorios"
            },
            {
                "nombre": "Mochila Escolar",
                "descripcion": "Mochila resistente con varios compartimentos",
                "precio": 75000,
                "stock_min": 10,
                "categoria": "Accesorios"
            },
            {
                "nombre": "Lámpara LED",
                "descripcion": "Lámpara decorativa para el hogar",
                "precio": 55000,
                "stock_min": 6,
                "categoria": "Hogar"
            }
        ]

        # Registrar productos
        for item in productos:

            existente = db.session.execute(
                db.select(Producto).where(
                    Producto.nombre == item["nombre"]
                )
            ).scalar_one_or_none()

            if existente:
                continue

            categoria = db.session.execute(
                db.select(Categoria).where(
                    Categoria.categoria_nombre == item["categoria"]
                )
            ).scalar_one()

            nuevo = Producto(
                nombre=item["nombre"],
                descripcion=item["descripcion"],
                precio=item["precio"],
                stock_min=item["stock_min"],
                categoria_id=categoria.categoria_id,
                disponible=True
            )

            db.session.add(nuevo)

        db.session.commit()

        print("================================")
        print("PRODUCTOS CARGADOS CORRECTAMENTE")
        print("================================")

        total = db.session.execute(
            db.select(Producto)
        ).scalars().all()

        print("Total de productos:", len(total))


if __name__ == "__main__":
    cargar_productos()
