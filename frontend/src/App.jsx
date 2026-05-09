import { BrowserRouter, Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import DetalheNascimento from "./pages/DetalheNascimento"
import Verificacao from "./pages/Verificacao"
import DashboardObitos from "./pages/DashboardObitos"
import DetalheObito from "./pages/DetalheObito"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/nascimento/:id" element={<DetalheNascimento />} />
        <Route path="/verificar" element={<Verificacao />} />
        <Route path="/obitos" element={<DashboardObitos />} />
        <Route path="/obito/:id" element={<DetalheObito />} />
      </Routes>
    </BrowserRouter>
  )
}
