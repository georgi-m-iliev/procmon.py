import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import flowbiteReact from "flowbite-react/plugin/vite";

// https://vite.dev/config/
export default defineConfig({
    content: ['./src/**/*.html', './node_modules/flowbite/**/*.js'],
    plugins: [react(), tailwindcss(), flowbiteReact()],
})