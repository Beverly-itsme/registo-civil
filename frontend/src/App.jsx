import { BrowserRouter, Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import DetalheNascimento from "./pages/DetalheNascimento"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/nascimento/:id" element={<DetalheNascimento />} />
      </Routes>
    </BrowserRouter>
  )
}
