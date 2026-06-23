<script setup>
defineProps({
  num: { type: String, default: '' },
  meta: { type: String, default: '' },
  eyebrow: { type: String, default: '' },
})
</script>

<template>
  <div class="slidev-layout" style="position: relative; height: 100%;">
    <div v-if="eyebrow" class="eyebrow">{{ eyebrow }}</div>
    <div style="margin-top: 48px; flex: 1; display: flex; flex-direction: column;">
      <slot />
    </div>
    <div class="slide-meta">
      <span>{{ num }}</span>
      <span>{{ meta }}</span>
    </div>
  </div>
</template>
