(() => {
	var cookie = (() => {
		if (!document.cookie) return undefined;
		var match = document.cookie.match(/\W?theme=(\w+)/);
		return match ? match[1] : undefined;
	})();

	var pathname = window.location.pathname;
	var isThemedPath =
		pathname.indexOf("/dashboard") === 0 ||
		pathname.indexOf("/login") === 0 ||
		pathname.indexOf("/onboarding") === 0 ||
		pathname.indexOf("/s/") === 0 ||
		pathname.indexOf("/embed/") === 0;
	var systemPrefersDark =
		typeof window.matchMedia === "function" &&
		window.matchMedia("(prefers-color-scheme: dark)").matches;
	var theme = cookie || (systemPrefersDark ? "dark" : "light");
	var applyTheme = () => {
		document.body.classList.add(theme);
	};

	if (isThemedPath) {
		if (document.body) {
			applyTheme();
		} else {
			window.addEventListener("DOMContentLoaded", applyTheme, { once: true });
		}
	}
})();
