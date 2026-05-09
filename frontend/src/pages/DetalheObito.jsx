import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import api from "../services/api"

export default function DetalheObito() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [registo, setRegisto] = useState(null)
  const [funcionario, setFuncionario] = useState("")
  const [motivo, setMotivo] = useState("")
  const [mensagem, setMensagem] = useState(null)
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    carregarRegisto()
  }, [id])

  async function carregarRegisto() {
    try {
      const resposta = await api.get(`/obitos/${id}`)
      setRegisto(resposta.data)
    } catch (erro) {
      console.error("Erro:", erro)
    }
    setCarregando(false)
  }

  async function aprovar() {
    if (!funcionario) {
      setMensagem({ tipo: "erro", texto: "Introduza o nome do funcionário!" })
      return
    }
    try {
      const resposta = await api.post("/obitos/aprovar", {
        pre_registo_id: parseInt(id),
        funcionario_nome: funcionario
      })
      if (resposta.data.sucesso) {
        setMensagem({ tipo: "sucesso", texto: `✅ Aprovado! NUIC: ${resposta.data.nuic}` })
        carregarRegisto()
      }
    } catch (erro) {
      setMensagem({ tipo: "erro", texto: "Erro ao aprovar!" })
    }
  }

  async function rejeitar() {
    if (!funcionario || !motivo) {
      setMensagem({ tipo: "erro", texto: "Introduza o nome do funcionário e o motivo!" })
      return
    }
    try {
      const resposta = await api.post("/obitos/rejeitar", {
        pre_registo_id: parseInt(id),
        funcionario_nome: funcionario,
        motivo: motivo
      })
      if (resposta.data.sucesso) {
        setMensagem({ tipo: "sucesso", texto: "❌ Registo rejeitado com sucesso." })
        carregarRegisto()
      }
    } catch (erro) {
      setMensagem({ tipo: "erro", texto: "Erro ao rejeitar!" })
    }
  }

  if (carregando) return <p style={{ padding: "20px" }}>A carregar...</p>
  if (!registo) return <p style={{ padding: "20px" }}>Registo não encontrado.</p>

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", background: "#f0f2f5", minHeight: "100vh" }}>
      <div style={{ maxWidth: "800px", margin: "0 auto" }}>

        <div style={{ background: "#1a5276", color: "white", padding: "20px", marginBottom: "20px", borderRadius: "8px" }}>
          <h1 style={{ margin: 0 }}>🕊️ Detalhe do Óbito #{id}</h1>
          <button onClick={() => navigate("/obitos")} style={{ marginTop: "10px", background: "transparent", color: "white", border: "1px solid white", padding: "6px 14px", borderRadius: "6px", cursor: "pointer" }}>
            ← Voltar
          </button>
        </div>

        {mensagem && (
          <div style={{ padding: "12px", borderRadius: "8px", marginBottom: "20px", background: mensagem.tipo === "sucesso" ? "#d5f5e3" : "#fadbd8", color: mensagem.tipo === "sucesso" ? "#1e8449" : "#c0392b" }}>
            {mensagem.texto}
          </div>
        )}

        <div style={{ background: "white", border: "1px solid #ddd", borderRadius: "8px", padding: "20px", marginBottom: "20px" }}>
          <h2 style={{ color: "#1a5276", marginTop: 0 }}>Dados do Óbito</h2>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <tbody>
              {[
                ["Estado", <span style={{ padding: "4px 10px", borderRadius: "12px", background: registo.estado === "aguarda_aprovacao" ? "#f39c12" : registo.estado === "aprovado" ? "#27ae60" : "#e74c3c", color: "white", fontSize: "12px" }}>{registo.estado.replace("_", " ")}</span>],
                ["Nome do falecido", registo.nome_falecido],
                ["BI do falecido", registo.bi_falecido],
                ["Data do óbito", new Date(registo.data_obito).toLocaleDateString("pt-PT")],
                ["Local do óbito", registo.local_obito],
                ["Causa do óbito", registo.causa_obito || "Não declarada"],
                ["Nome do declarante", registo.nome_declarante],
                ["BI do declarante", registo.bi_declarante],
                ["Contacto", registo.contacto_declarante],
                ["Email", registo.email_declarante || "Não fornecido"],
              ].map(([label, valor]) => (
                <tr key={label} style={{ borderBottom: "1px solid #eee" }}>
                  <td style={{ padding: "10px", fontWeight: "bold", color: "#555", width: "40%" }}>{label}</td>
                  <td style={{ padding: "10px" }}>{valor}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {registo.estado === "aguarda_aprovacao" && (
          <div style={{ background: "white", border: "1px solid #ddd", borderRadius: "8px", padding: "20px" }}>
            <h2 style={{ color: "#1a5276", marginTop: 0 }}>Decisão do Funcionário</h2>

            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", fontWeight: "bold", marginBottom: "6px" }}>Nome do funcionário *</label>
              <input
                value={funcionario}
                onChange={e => setFuncionario(e.target.value)}
                placeholder="Ex: Dr. Carlos Machava"
                style={{ width: "100%", padding: "10px", borderRadius: "6px", border: "1px solid #ddd", fontSize: "14px", boxSizing: "border-box" }}
              />
            </div>

            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", fontWeight: "bold", marginBottom: "6px" }}>Motivo de rejeição (só se rejeitar)</label>
              <textarea
                value={motivo}
                onChange={e => setMotivo(e.target.value)}
                placeholder="Ex: Dados inconsistentes com o BI"
                rows={3}
                style={{ width: "100%", padding: "10px", borderRadius: "6px", border: "1px solid #ddd", fontSize: "14px", boxSizing: "border-box" }}
              />
            </div>

            <div style={{ display: "flex", gap: "12px" }}>
              <button onClick={aprovar} style={{ flex: 1, padding: "12px", background: "#27ae60", color: "white", border: "none", borderRadius: "8px", fontSize: "16px", cursor: "pointer", fontWeight: "bold" }}>
                ✅ Aprovar Óbito
              </button>
              <button onClick={rejeitar} style={{ flex: 1, padding: "12px", background: "#e74c3c", color: "white", border: "none", borderRadius: "8px", fontSize: "16px", cursor: "pointer", fontWeight: "bold" }}>
                ❌ Rejeitar Óbito
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
} 
