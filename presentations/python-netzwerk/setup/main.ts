/* Slidev setup/main.ts entry — must default-export the configuration. */
import { defineAppSetup } from '@slidev/types'
import '../style.css'

export default defineAppSetup(({ app, router }) => {
  // Hook point for app-level setup (Vue plugins, route guards, etc.).
  // Empty for now; the import above is what we need so styles load.
})
