import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import api from "../services/api"

export default function DashboardObitos() {
  const navigate = useNavigate()
  const [obitos, setObitos] = useState([])
  const [filtro, setFiltro] = useState("aguarda_aprovacao")
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    carregarObitos()
  }, [filtro])

  async function carregarObitos() {
    setCarregando(true)
    try {
      const resposta = await api.get(`/obitos/lista?estado=${filtro}`)
      setObitos(resposta.data.registos)
    } catch (erro) {
      console.error("Erro ao carregar:", erro)
    }
    setCarregando(false)
  }

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", background: "#f0f2f5", minHeight: "100vh" }}>

      <div style={{ background: "#1a5276", color: "white", padding: "20px", marginBottom: "20px", borderRadius: "8px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0 }}>🏛️ Conservatória do Registo Civil de Beira</h1>
          <p style={{ margin: "5px 0 0 0", opacity: 0.8 }}>Painel de Óbitos</p>
        </div>
        <div style={{ display: "flex", gap: "10px" }}>
          <button onClick={() => navigate("/")} style={{ background: "transparent", color: "white", border: "1px solid white", padding: "8px 16px", borderRadius: "6px", cursor: "pointer" }}>
            Nascimentos
          </button>
          <button onClick={() => navigate("/verificar")} style={{ background: "transparent", color: "white", border: "1px solid white", padding: "8px 16px", borderRadius: "6px", cursor: "pointer" }}>
            🔍 Verificação
          </button>
        </div>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <strong>Filtrar por estado:</strong>
        <div style={{ display: "flex", gap: "10px", marginTop: "10px", flexWrap: "wrap" }}>
          {["aguarda_aprovacao", "aprovado", "rejeitado"].map(estado => (
            <button
              key={estado}
              onClick={() => setFiltro(estado)}
              style={{
                padding: "8px 16px",
                borderRadius: "20px",
                border: "none",
                cursor: "pointer",
                background: filtro === estado ? "#1a5276" : "#ddd",
                color: filtro === estado ? "white" : "black",
                fontWeight: filtro === estado ? "bold" : "normal"
              }}
            >
              {estado.replace("_", " ").toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {carregando ? (
        <p>A carregar...</p>
      ) : obitos.length === 0 ? (
        <p style={{ color: "#888" }}>Nenhum registo encontrado com este estado.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse", background: "white", borderRadius: "8px", overflow: "hidden" }}>
          <thead>
            <tr style={{ background: "#1a5276", color: "white" }}>
              <th style={{ padding: "12px", textAlign: "left" }}>ID</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Nome do Falecido</th>
              <th style={{ padding: "12px", textAlign: "left" }}>BI</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Data Óbito</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Estado</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Acção</th>
            </tr>
          </thead>
          <tbody>
            {obitos.map((r, i) => (
              <tr key={r.id} style={{ background: i % 2 === 0 ? "#f9f9f9" : "white" }}>
                <td style={{ padding: "12px" }}>{r.id}</td>
                <td style={{ padding: "12px" }}>{r.nome_falecido}</td>
                <td style={{ padding: "12px" }}>{r.bi_falecido}</td>
                <td style={{ padding: "12px" }}>{new Date(r.data_obito).toLocaleDateString("pt-PT")}</td>
                <td style={{ padding: "12px" }}>
                  <span style={{
                    padding: "4px 10px",
                    borderRadius: "12px",
                    fontSize: "12px",
                    background: r.estado === "aguarda_aprovacao" ? "#f39c12" :
                                r.estado === "aprovado" ? "#27ae60" : "#e74c3c",
                    color: "white"
                  }}>
                    {r.estado.replace("_", " ")}
                  </span>
                </td>
                <td style={{ padding: "12px" }}>
                  <a href={`/obito/${r.id}`} style={{ color: "#1a5276", textDecoration: "none", fontWeight: "bold" }}>
                    Ver detalhes →
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
} 
