import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],

  // Build configuration
  build: {
    rollupOptions: {
      input: {
        // Define multiple entry points for the application
        landing: "src/landing/main.jsx",
        protected: "src/protected/main.jsx",
      },
    },

    // Specify build output directory relative to project root
    // '../backend/build' indicates the build files will go in the backend directory
    outDir: "../backend/build",

    // Generate a manifest.json file that maps source files to their output bundles
    // This is used by the Flask backend in prod to locate the correct asset files
    manifest: true,
  },

  // Development server configuration
  server: {
    // Set development server port
    port: 3000,
    proxy: {
      // Forward all /api requests to the Flask backend
      "/api": {
        target: "http://localhost:8000",  // Flask server address
        changeOrigin: true,  // Changes the origin of the request to match the target URL
      },
    },
  },
});
