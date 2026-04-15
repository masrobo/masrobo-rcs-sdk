function requireValue(value, name) {
  if (value == null) {
    throw new Error(`${name} is required`);
  }
  if (typeof value === 'string' && !value.trim()) {
    throw new Error(`${name} is required`);
  }
}

module.exports = { requireValue };

