import { useState, useEffect } from "react"
import api from "../services/api"

export default function Dashboard() {
  const [nascimentos, setNascimentos] = useState([])
  const [filtro, setFiltro] = useState("aguarda_aprovacao")
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    carregarNascimentos()
  }, [filtro])

  async function carregarNascimentos() {
    setCarregando(true)
    try {
      const resposta = await api.get(`/nascimentos/lista?estado=${filtro}`)
      setNascimentos(resposta.data.registos)
    } catch (erro) {
      console.error("Erro ao carregar:", erro)
    }
    setCarregando(false)
  }

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>

      <div style={{ background: "#1a5276", color: "white", padding: "20px", marginBottom: "20px", borderRadius: "8px" }}>
        <h1 style={{ margin: 0 }}>🏛️ Conservatória do Registo Civil de Beira</h1>
        <p style={{ margin: "5px 0 0 0", opacity: 0.8 }}>Painel do Funcionário</p>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <strong>Filtrar por estado:</strong>
        <div style={{ display: "flex", gap: "10px", marginTop: "10px", flexWrap: "wrap" }}>
          {["aguarda_aprovacao", "incompleto", "aprovado", "rejeitado"].map(estado => (
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
      ) : nascimentos.length === 0 ? (
        <p style={{ color: "#888" }}>Nenhum registo encontrado com este estado.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#1a5276", color: "white" }}>
              <th style={{ padding: "12px", textAlign: "left" }}>ID</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Nome da Criança</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Nome da Mãe</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Data Nascimento</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Estado</th>
              <th style={{ padding: "12px", textAlign: "left" }}>Acção</th>
            </tr>
          </thead>
          <tbody>
            {nascimentos.map((r, i) => (
              <tr key={r.id} style={{ background: i % 2 === 0 ? "#f9f9f9" : "white" }}>
                <td style={{ padding: "12px" }}>{r.id}</td>
                <td style={{ padding: "12px" }}>{r.nome_completo_crianca || "Não definido"} {r.apelidos_crianca || ""}</td>
                <td style={{ padding: "12px" }}>{r.nome_mae}</td>
                <td style={{ padding: "12px" }}>{new Date(r.data_nascimento).toLocaleDateString("pt-PT")}</td>
                <td style={{ padding: "12px" }}>
                  <span style={{
                    padding: "4px 10px",
                    borderRadius: "12px",
                    fontSize: "12px",
                    background: r.estado === "aguarda_aprovacao" ? "#f39c12" :
                                r.estado === "aprovado" ? "#27ae60" :
                                r.estado === "rejeitado" ? "#e74c3c" : "#95a5a6",
                    color: "white"
                  }}>
                    {r.estado.replace("_", " ")}
                  </span>
                </td>
                <td style={{ padding: "12px" }}>
                  <a href={`/nascimento/${r.id}`} style={{ color: "#1a5276", textDecoration: "none", fontWeight: "bold" }}>
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
