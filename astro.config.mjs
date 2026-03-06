import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
    // Static site — outputs pure HTML to dist/
    output: 'static',

    // Build output directory
    outDir: './dist',

    // Public asset directory (animations, images, shared JS)
    publicDir: './public',

    // GitHub Pages: set base to '/<repo-name>' if deploying to a subdirectory
    // base: '/SysDes',  // uncomment if needed for GitHub Pages subpath

    build: {
        // Don't inline assets smaller than threshold
        assetsPrefix: './',
    },

    // Vite server config for local dev
    vite: {
        server: {
            port: 4321,
        },
    },
});
