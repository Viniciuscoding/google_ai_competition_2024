import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteStaticCopy } from 'vite-plugin-static-copy';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    viteStaticCopy({
      targets: [
        {
          src: 'public/manifest.json',
          dest: './',
        }
      ],
    }),
  ],
  base: './', 
  build: {
    outDir: 'build',
    rollupOptions: {
      input: {
        popup: './index.html',
      },
      output: {
        entryFileNames: '[name].js', // Ensures the service worker and popup.js stay unminified
      },
    },
  },
});
