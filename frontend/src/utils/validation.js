export function validateEmail(email) {
  // Email validation regex pattern
  const emailPattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}));?$/
  return emailPattern.test(email)
}

export function validatePassword(password) {
  // Password validation regex pattern (at least 6 characters)
  const passwordPattern = /^.{6,}$/
  return passwordPattern.test(password)
}