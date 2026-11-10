import { useEffect, useRef } from 'react'
import markup from './markup.html?raw'
import init from './init.js'
import './portfolio.css'

// The page is a single static layout; init() wires up its animations and dynamic sections.
export default function Portfolio() {
  const started = useRef(false)
  useEffect(() => {
    if (started.current) return
    started.current = true
    init()
  }, [])
  return <div className="site" dangerouslySetInnerHTML={{ __html: markup }} />
}
