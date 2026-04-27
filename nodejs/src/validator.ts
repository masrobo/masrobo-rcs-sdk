export function requireValue(value: any, name: string): void {
  if (value == null) {
    throw new Error(`${name} is required`);
  }
  if (typeof value === 'string' && !value.trim()) {
    throw new Error(`${name} is required`);
  }
}