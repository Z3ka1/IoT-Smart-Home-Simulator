
export const truncateText = (text, maxLength, fallback = '') => {
  const value = text || fallback
  return value.length > maxLength ? value.substring(0, maxLength) + '...' : value
}

export const truncateDescription = (text, maxLength, fallback = '') => {
  const value = text || fallback
  return value.length > maxLength ? fallback : value
}