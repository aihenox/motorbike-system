(function () {
    "use strict";

    const meta = document.querySelector('meta[name="csrf-token"]');

    if (!meta) {
        return;
    }

    const token = meta.content;
    const unsafeMethods = new Set(["POST", "PUT", "PATCH", "DELETE"]);
    const originalFetch = window.fetch.bind(window);

    window.fetch = function (input, options) {
        const config = options ? { ...options } : {};
        const request = input instanceof Request ? input : null;
        const method = String(
            config.method || (request && request.method) || "GET"
        ).toUpperCase();
        const url = new URL(
            request ? request.url : input,
            window.location.href
        );

        if (url.origin === window.location.origin && unsafeMethods.has(method)) {
            const headers = new Headers(request ? request.headers : undefined);
            new Headers(config.headers || {}).forEach((value, key) => {
                headers.set(key, value);
            });
            headers.set("X-CSRF-Token", token);
            config.headers = headers;
        }

        return originalFetch(input, config);
    };

    document.addEventListener("submit", function (event) {
        const form = event.target;
        const method = String(form.method || "GET").toUpperCase();

        if (!unsafeMethods.has(method)) {
            return;
        }

        let field = form.querySelector('input[name="_csrf_token"]');

        if (!field) {
            field = document.createElement("input");
            field.type = "hidden";
            field.name = "_csrf_token";
            form.appendChild(field);
        }

        field.value = token;
    }, true);
})();
