import { describe, it, expect } from 'vitest';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { UNIDADES, porSlug } from './unidades.ts';

const aqui = dirname(fileURLToPath(import.meta.url));
const PUBLIC = resolve(aqui, '../../public');

describe('Datos de unidades Senna', () => {
  it('hay al menos las dos unidades', () => {
    expect(UNIDADES.length).toBeGreaterThanOrEqual(2);
  });

  it('los slugs son únicos', () => {
    const slugs = UNIDADES.map((u) => u.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
  });

  it('cada unidad tiene los campos obligatorios con contenido', () => {
    for (const u of UNIDADES) {
      expect(u.nombre.trim()).not.toBe('');
      expect(u.numero.trim()).not.toBe('');
      expect(u.ubicacion.trim()).not.toBe('');
      expect(u.distribucion.trim()).not.toBe('');
      expect(u.resumen.length).toBeGreaterThan(20);
      expect(u.amenidades.length).toBeGreaterThan(0);
    }
  });

  it('el equipamiento es Full o Semifull', () => {
    for (const u of UNIDADES) {
      expect(['Full', 'Semifull']).toContain(u.equipamiento);
    }
  });

  it('el precio trae monto y nota no vacíos', () => {
    for (const u of UNIDADES) {
      expect(u.precio.monto.trim()).not.toBe('');
      expect(u.precio.nota.trim()).not.toBe('');
    }
  });

  it('porSlug encuentra y discrimina correctamente', () => {
    expect(porSlug('requinoa')?.nombre).toContain('Requínoa');
    expect(porSlug('no-existe')).toBeUndefined();
  });

  it('las imágenes locales referenciadas existen en /public', () => {
    for (const u of UNIDADES) {
      const refs = [u.destacada, ...u.galeria];
      for (const img of refs) {
        if (img.src.startsWith('/')) {
          const ruta = resolve(PUBLIC, '.' + img.src);
          expect(existsSync(ruta), `Falta la imagen ${img.src}`).toBe(true);
        }
        expect(img.alt.trim(), `Falta alt en ${img.src}`).not.toBe('');
      }
    }
  });
});
