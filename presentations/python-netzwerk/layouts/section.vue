<script setup>
defineProps({
  num: { type: String, required: true },
  kicker: { type: String, default: 'Section' },
  meta: { type: String, default: '' },
})
</script>

<template>
  <div class="slidev-layout deep" style="position: relative; height: 100%; padding: 0;">
    <div class="grid-bg" style="opacity: 0.25"></div>
    <div style="position: relative; padding: 100px 110px; height: 100%; display: flex; flex-direction: column; justify-content: center; gap: 40px;">
      <div style="display: flex; align-items: baseline; gap: 32px;">
        <span class="mono accent" style="font-size: 140px; font-weight: 500; letter-spacing: -0.04em; line-height: 1;">{{ num }}</span>
        <span class="mono muted" style="font-size: 26px; letter-spacing: 0.18em; text-transform: uppercase;">{{ kicker }}</span>
      </div>
      <slot />
      <div class="slide-meta">
        <span>PART {{ num }}</span>
        <span>{{ meta || kicker }}</span>
      </div>
    </div>
  </div>
</template>
