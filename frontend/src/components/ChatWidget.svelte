<script>
  // Widget de chat Senna. Habla con el backend FastAPI (/chat). Si el backend
  // no está disponible, ofrece WhatsApp como fallback. No inventa respuestas:
  // el cerebro vive en el servidor.
  export let wpp = '56966078526';
  const API = import.meta.env.PUBLIC_API_URL ?? 'http://localhost:8000';

  let abierto = false;
  let cargando = false;
  let texto = '';
  let mensajes = [
    { rol: 'asistente', texto: 'Hola 👋 Soy el asistente de Senna. ¿Te muestro las unidades, precios o disponibilidad?' },
  ];

  async function enviar() {
    const limpio = texto.trim();
    if (!limpio || cargando) return;
    mensajes = [...mensajes, { rol: 'usuario', texto: limpio }];
    texto = '';
    cargando = true;
    try {
      const r = await fetch(`${API}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensajes }),
      });
      if (!r.ok) throw new Error('sin servicio');
      const data = await r.json();
      mensajes = [...mensajes, { rol: 'asistente', texto: data.respuesta }];
    } catch {
      mensajes = [...mensajes, {
        rol: 'asistente',
        texto: 'No pude conectar ahora mismo. Escríbenos directo por WhatsApp y te respondemos al toque.',
        wpp: true,
      }];
    } finally {
      cargando = false;
    }
  }
</script>

{#if abierto}
  <div class="panel" role="dialog" aria-label="Asistente Senna">
    <div class="panel__top">
      <span>Asistente Senna</span>
      <button class="x" on:click={() => (abierto = false)} aria-label="Cerrar">×</button>
    </div>
    <div class="panel__msgs">
      {#each mensajes as m}
        <div class="msg msg--{m.rol}">
          {m.texto}
          {#if m.wpp}
            <a class="msg__wpp" href={`https://wa.me/${wpp}`}>Abrir WhatsApp →</a>
          {/if}
        </div>
      {/each}
      {#if cargando}<div class="msg msg--asistente">…</div>{/if}
    </div>
    <form class="panel__input" on:submit|preventDefault={enviar}>
      <input bind:value={texto} placeholder="Escribe tu consulta…" aria-label="Mensaje" />
      <button class="boton" type="submit" disabled={cargando}>Enviar</button>
    </form>
  </div>
{/if}

<button class="fab" on:click={() => (abierto = !abierto)} aria-label="Abrir chat">
  {abierto ? '×' : 'Chat'}
</button>

<style>
  .fab {
    position: fixed; right: 22px; bottom: 22px; z-index: 60;
    background: var(--oro); color: var(--noche); border: none;
    font-weight: 600; font-size: 15px; padding: 14px 20px; border-radius: 999px;
    cursor: pointer; box-shadow: 0 10px 30px rgba(0,0,0,0.45);
  }
  .panel {
    position: fixed; right: 22px; bottom: 84px; z-index: 60;
    width: min(360px, calc(100vw - 44px)); height: 460px; display: flex; flex-direction: column;
    background: var(--profundo); border: 1px solid var(--linea); border-radius: 8px;
    overflow: hidden; box-shadow: 0 24px 60px rgba(0,0,0,0.55);
  }
  .panel__top { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-bottom: 1px solid var(--linea); font-family: var(--fuente-display); }
  .x { background: none; border: none; color: var(--acero); font-size: 22px; cursor: pointer; }
  .panel__msgs { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 10px; }
  .msg { padding: 10px 13px; border-radius: 10px; font-size: 14px; max-width: 85%; }
  .msg--asistente { background: rgba(245,244,240,0.06); align-self: flex-start; }
  .msg--usuario { background: var(--oro); color: var(--noche); align-self: flex-end; }
  .msg__wpp { display: block; margin-top: 6px; color: var(--oro); font-weight: 600; }
  .panel__input { display: flex; gap: 8px; padding: 12px; border-top: 1px solid var(--linea); }
  .panel__input input { flex: 1; background: var(--noche); border: 1px solid var(--linea); color: var(--marfil); border-radius: 6px; padding: 10px 12px; font-family: inherit; }
  .panel__input .boton { padding: 10px 16px; }
</style>
