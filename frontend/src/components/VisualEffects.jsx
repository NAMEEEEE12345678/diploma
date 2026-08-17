import { useEffect, useRef, useState } from "react";

export function TiltCard({ children, className = "" }) {
  const ref = useRef(null);
  function move(event) {
    if (!ref.current || window.matchMedia("(pointer: coarse)").matches) return;
    const rect = ref.current.getBoundingClientRect();
    ref.current.style.setProperty("--rx", `${((event.clientY - rect.top) / rect.height - .5) * -8}deg`);
    ref.current.style.setProperty("--ry", `${((event.clientX - rect.left) / rect.width - .5) * 9}deg`);
    ref.current.style.setProperty("--mx", `${((event.clientX - rect.left) / rect.width) * 100}%`);
  }
  return <div ref={ref} className={`tilt-card ${className}`} onMouseMove={move} onMouseLeave={() => ref.current?.style.setProperty("--rx","0deg")}>{children}</div>;
}

export function Reveal({ children, className = "" }) {
  const ref = useRef(null); const [visible,setVisible] = useState(false);
  useEffect(()=>{const observer=new IntersectionObserver(([entry])=>entry.isIntersecting&&setVisible(true),{threshold:.12});if(ref.current)observer.observe(ref.current);return()=>observer.disconnect()},[]);
  return <div ref={ref} className={`reveal ${visible?"reveal--visible":""} ${className}`}>{children}</div>;
}
