import styled from 'styled-components'

export const Button = styled.button<{ $variant?: 'primary' | 'ghost' }>`
  height: 36px;
  padding: 0 14px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid ${(p) => (p.$variant === 'ghost' ? '#d4d4d8' : 'transparent')};
  background: ${(p) => (p.$variant === 'ghost' ? 'transparent' : '#18181b')};
  color: ${(p) => (p.$variant === 'ghost' ? '#18181b' : '#fafafa')};

  &:hover { opacity: 0.9; }
  &:disabled { opacity: 0.5; cursor: not-allowed; }
`
