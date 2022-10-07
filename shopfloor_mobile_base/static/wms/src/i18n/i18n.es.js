/**
 * Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
 * @author Simone Orsi <simahawk@gmail.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
 */

import {translation_registry} from "../services/translation_registry.js";

const messages_en = {
    screen: {
        login: {
            title: "Login",
            action: {
                login: "Login",
            },
            error: {
                login_invalid: "Credenciales inválidas",
            },
        },
        home: {
            title: "Inicio",
            main_title: "Inicio",
            version: "Version:",
            action: {
                nuke_data_and_reload: "Forzar la recarga de datos y refrescar",
            },
        },
        scan_anything: {
            name: "Scanear",
            title: "Scanear {con}",
            scan_placeholder: "Scanear algo",
        },
        settings: {
            title: "Ajustes",
            home: {
                name: "Ajustes",
                title: "Ajustes",
            },
            language: {
                name: "Idioma",
                title: "Seleccionar idioma",
            },
            profile: {
                name: "Perfile",
                title: "Seleccionar perfil",
                profile_updated: "Perfil actualizado",
            },
            fullscreen: {
                enter: "Pantalla completa",
                exit: "Salir pantalla completa",
            },
        },
    },
    app: {
        profile_not_configured: "No ha configurado su perfil. Indique uno, por favor.",
        profile_configure: "Configuración perfil",
        loading: "Cargando...",
        action: {
            logout: "Salir",
        },
        nav: {
            scenario: "Escenario:",
            op_types: "Tipos op:",
        },
        log_entry_link: "Ver / compartir entradas log",
        running_env: {
            prod: "Production",
            integration: "Integration",
            staging: "Staging",
            test: "Test",
            dev: "Development",
        },
    },
    language: {
        name: {
            English: "English",
            French: "French",
            German: "German",
            Spanish: "Español",
        },
    },
    btn: {
        back: {
            title: "Atrás",
        },
        confirm: {
            title: "Confirmar",
        },
        ok: {
            title: "Ok",
        },
        reset: {
            title: "Reset",
        },
        cancel: {
            title: "Cancelar",
        },
        reload_config: {
            title: "Recargar configuración y menú",
        },
    },
    misc: {
        // TODO: split out WMS messages
        btn_get_work: "Obtener tareas",
        btn_manual_selection: "Selectción manual",
        stock_zero_check: {
            confirm_stock_zero: "Confirmar stock = 0",
            confirm_stock_not_zero: "Declarar stock no vacío",
        },
        actions_popup: {
            btn_action: "Acción",
        },
        lines_count: "{priority_lines_count}/{lines_count}",
        lines_count_extended: "{priority_lines_count}/{lines_count} position(es)",
        picking_count: "{priority_picking_count}/{picking_count}",
        picking_count_extended: "{priority_picking_count}/{picking_count} albarán(es)",
    },
    list: {
        no_items: "Sin datos.",
    },
    select: {
        no_items: "No ha seleccionado nada.",
    },
    order_lines_by: {
        priority: "Ordenar por prioridad",
        location: "Ordenar por ubicación",
    },
};

translation_registry.add("es-ES", messages_en);
