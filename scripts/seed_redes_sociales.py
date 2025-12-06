"""
Script para poblar la base de datos con tipos de redes sociales comunes.
Ejecutar con: python -m scripts.seed_redes_sociales
"""

import asyncio
from sqlmodel import select
from app.core.database import async_session_maker
from app.models import CatalogoRedSocial


# Tipos de redes sociales comunes con iconos Font Awesome
REDES_SOCIALES_COMUNES = [
    {
        "nombre": "Twitter / X",
        "icono_font_awesome": "fa-brands fa-x-twitter",
        "url_placeholder": "https://twitter.com/tu_usuario",
    },
    {
        "nombre": "Facebook",
        "icono_font_awesome": "fa-brands fa-facebook",
        "url_placeholder": "https://facebook.com/tu_usuario",
    },
    {
        "nombre": "Instagram",
        "icono_font_awesome": "fa-brands fa-instagram",
        "url_placeholder": "https://instagram.com/tu_usuario",
    },
    {
        "nombre": "LinkedIn",
        "icono_font_awesome": "fa-brands fa-linkedin",
        "url_placeholder": "https://linkedin.com/in/tu_usuario",
    },
    {
        "nombre": "GitHub",
        "icono_font_awesome": "fa-brands fa-github",
        "url_placeholder": "https://github.com/tu_usuario",
    },
    {
        "nombre": "YouTube",
        "icono_font_awesome": "fa-brands fa-youtube",
        "url_placeholder": "https://youtube.com/@tu_canal",
    },
    {
        "nombre": "TikTok",
        "icono_font_awesome": "fa-brands fa-tiktok",
        "url_placeholder": "https://tiktok.com/@tu_usuario",
    },
    {
        "nombre": "Threads",
        "icono_font_awesome": "fa-brands fa-threads",
        "url_placeholder": "https://threads.net/@tu_usuario",
    },
    {
        "nombre": "WhatsApp",
        "icono_font_awesome": "fa-brands fa-whatsapp",
        "url_placeholder": "https://wa.me/tunumero",
    },
    {
        "nombre": "Telegram",
        "icono_font_awesome": "fa-brands fa-telegram",
        "url_placeholder": "https://t.me/tu_usuario",
    },
    {
        "nombre": "Discord",
        "icono_font_awesome": "fa-brands fa-discord",
        "url_placeholder": "https://discord.gg/tu_servidor",
    },
    {
        "nombre": "Twitch",
        "icono_font_awesome": "fa-brands fa-twitch",
        "url_placeholder": "https://twitch.tv/tu_canal",
    },
    {
        "nombre": "Reddit",
        "icono_font_awesome": "fa-brands fa-reddit",
        "url_placeholder": "https://reddit.com/u/tu_usuario",
    },
    {
        "nombre": "Pinterest",
        "icono_font_awesome": "fa-brands fa-pinterest",
        "url_placeholder": "https://pinterest.com/tu_usuario",
    },
    {
        "nombre": "Spotify",
        "icono_font_awesome": "fa-brands fa-spotify",
        "url_placeholder": "https://open.spotify.com/user/tu_usuario",
    },
    {
        "nombre": "Medium",
        "icono_font_awesome": "fa-brands fa-medium",
        "url_placeholder": "https://medium.com/@tu_usuario",
    },
    {
        "nombre": "Dev.to",
        "icono_font_awesome": "fa-brands fa-dev",
        "url_placeholder": "https://dev.to/tu_usuario",
    },
    {
        "nombre": "Stack Overflow",
        "icono_font_awesome": "fa-brands fa-stack-overflow",
        "url_placeholder": "https://stackoverflow.com/users/tu_id",
    },
    {
        "nombre": "Sitio Web",
        "icono_font_awesome": "fa-solid fa-globe",
        "url_placeholder": "https://tusitio.com",
    },
]


async def seed_redes_sociales():
    """Poblar la base de datos con tipos de redes sociales comunes."""
    async with async_session_maker() as session:
        # Verificar si ya existen datos
        result = await session.execute(select(CatalogoRedSocial))
        existentes = result.scalars().all()

        if existentes:
            print(
                f"⚠️  Ya existen {len(existentes)} tipos de redes sociales en la base de datos."
            )
            respuesta = input("¿Deseas agregar más tipos? (s/n): ")
            if respuesta.lower() != "s":
                print("❌ Operación cancelada.")
                return

        # Crear tipos de redes sociales
        tipos_creados = 0
        for red_data in REDES_SOCIALES_COMUNES:
            # Verificar si ya existe
            result = await session.execute(
                select(CatalogoRedSocial).where(
                    CatalogoRedSocial.nombre == red_data["nombre"]
                )
            )
            existente = result.scalars().first()

            if not existente:
                tipo = CatalogoRedSocial(**red_data, activo=True)
                session.add(tipo)
                tipos_creados += 1
                print(f"✅ Creado: {red_data['nombre']}")
            else:
                print(f"⏭️  Ya existe: {red_data['nombre']}")

        # Guardar cambios
        await session.commit()
        print(
            f"\n🎉 Proceso completado. {tipos_creados} tipos de redes sociales creados."
        )


if __name__ == "__main__":
    print("🚀 Iniciando seed de tipos de redes sociales...\n")
    asyncio.run(seed_redes_sociales())
