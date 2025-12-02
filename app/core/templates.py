from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")


def user_initials(user) -> str:
    try:
        nombres = getattr(user, "nombres", None) or ""
        apellidos = getattr(user, "apellidos", None) or ""
        if nombres or apellidos:
            firsts = []
            if nombres:
                firsts.append(nombres.split()[0])
            if apellidos:
                firsts.append(apellidos.split()[0])
            return "".join([p[0].upper() for p in firsts if p])
        username = getattr(user, "username", "")
        return (username[:2].upper()) if username else "?"
    except Exception:
        return "?"

templates.env.globals["user_initials"] = user_initials
