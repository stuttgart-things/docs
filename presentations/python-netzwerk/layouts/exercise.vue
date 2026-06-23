<script setup>
defineProps({
  num: { type: String, default: '' },
  meta: { type: String, default: '' },
  zeit: { type: String, default: '' },
  datei: { type: String, default: '' },
})
</script>

<template>
  <div class="slidev-layout is-exercise" style="position: relative; height: 100%;">
    <div class="exercise-badge">★ Übung</div>
    <div style="margin-top: 40px; flex: 1; display: flex; flex-direction: column;">
      <slot />
    </div>
    <div class="slide-meta">
      <span>{{ num }}</span>
      <span>
        <template v-if="datei"><span class="mono">{{ datei }}</span></template>
        <template v-if="datei && zeit"> · </template>
        <template v-if="zeit">⏱ {{ zeit }}</template>
        <template v-if="!datei && !zeit">{{ meta }}</template>
      </span>
    </div>
  </div>
</template>
