import { useEffect, useRef } from 'react'

declare global {
  interface Window {
    MathJax?: {
      Hub: {
        Queue: (command: any[]) => void
        Typeset: (element?: HTMLElement) => void
      }
    }
  }
}

export function MathText({ children, style }: { children: string; style?: React.CSSProperties }) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (containerRef.current && window.MathJax) {
      // Queue MathJax to typeset this specific element
      window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, containerRef.current])
    }
  }, [children])

  return (
    <div ref={containerRef} style={style}>
      {children}
    </div>
  )
}
