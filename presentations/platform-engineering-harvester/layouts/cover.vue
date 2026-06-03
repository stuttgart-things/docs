<script setup>
const props = defineProps({
  num: { type: String, default: '' },
  meta: { type: String, default: '' },
})
</script>

<template>
  <div class="slidev-layout deep" style="position: relative; height: 100%; padding: 0;">
    <div class="grid-bg" style="opacity: 0.25"></div>
    <div style="position: relative; padding: 100px 110px; height: 100%; display: flex; flex-direction: column;">
      <slot />
      <div class="slide-meta">
        <span>{{ num }}</span>
        <span>{{ meta }}</span>
      </div>
    </div>
  </div>
</template>
