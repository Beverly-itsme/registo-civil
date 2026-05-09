import { useState } from "react"
import { useNavigate } from "react-router-dom"
import api from "../services/api"

export default function Verificacao() {
  const navigate = useNavigate()
  const [nuic, setNuic] = useState("")
  const [resultado, setResultado] = useState(null)
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState(null)

  async function verificar() {
    if (!nuic.trim()) {
      setErro("Introduza um NUIC válido!")
      return
    }
    setCarregando(true)
    setErro(null)
    setResultado(null)
    try {
      const resposta = await api.get(`/verificar/${nuic.trim()}`)
      setResultado(resposta.data)
    } catch (e) {
      setErro("Erro ao consultar. Tente novamente.")
    }
    setCarregando(false)
  }

  return (
    <div style={{ minHeight: "100vh", background: "#f0f2f5", fontFamily: "Segoe UI, Arial, sans-serif" }}>

      <div style={{ background: "#1a5276", color: "white", padding: "20px 40px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0, fontSize: "20px" }}>🏛️ Conservatória do Registo Civil de Beira</h1>
          <p style={{ margin: "4px 0 0 0", opacity: 0.8, fontSize: "13px" }}>Verificação Pública de Registos</p>
        </div>
        <button onClick={() => navigate("/")} style={{ background: "transparent", color: "white", border: "1px solid white", padding: "8px 16px", borderRadius: "6px", cursor: "pointer" }}>
          Painel do Funcionário
        </button>
      </div>

      <div style={{ maxWidth: "600px", margin: "60px auto", padding: "0 20px" }}>

        <div style={{ background: "white", borderRadius: "12px", padding: "40px", boxShadow: "0 2px 12px rgba(0,0,0,0.08)" }}>
          <h2 style={{ color: "#1a5276", marginBottom: "8px", textAlign: "center" }}>🔍 Consultar Registo</h2>
          <p style={{ color: "#888", textAlign: "center", marginBottom: "30px", fontSize: "14px" }}>
            Introduza o NUIC para consultar os dados básicos do registo civil
          </p>

          <div style={{ display: "flex", gap: "10px" }}>
            <input
              value={nuic}
              onChange={e => setNuic(e.target.value.toUpperCase())}
              onKeyDown={e => e.key === "Enter" && verificar()}
              placeholder="Ex: NASC-2026-000001"
              style={{ flex: 1, padding: "12px 16px", borderRadius: "8px", border: "1px solid #ddd", fontSize: "15px", outline: "none" }}
            />
            <button
              onClick={verificar}
              disabled={carregando}
              style={{ padding: "12px 24px", background: "#1a5276", color: "white", border: "none", borderRadius: "8px", cursor: "pointer", fontSize: "15px", fontWeight: "bold" }}
            >
              {carregando ? "..." : "Consultar"}
            </button>
          </div>

          {erro && (
            <p style={{ color: "#e74c3c", marginTop: "12px", textAlign: "center" }}>{erro}</p>
          )}
        </div>

        {resultado && (
          <div style={{ background: "white", borderRadius: "12px", padding: "30px", boxShadow: "0 2px 12px rgba(0,0,0,0.08)", marginTop: "20px" }}>

            {resultado.encontrado ? (
              <>
                <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "24px" }}>
                  <span style={{ fontSize: "40px" }}>{resultado.tipo === "nascimento" ? "👶" : "🕊️"}</span>
                  <div>
                    <h3 style={{ margin: 0, color: "#1a5276" }}>Registo Encontrado</h3>
                    <span style={{ padding: "4px 12px", borderRadius: "12px", fontSize: "12px", background: resultado.tipo === "nascimento" ? "#d5f5e3" : "#fdebd0", color: resultado.tipo === "nascimento" ? "#1e8449" : "#d35400" }}>
                      {resultado.tipo === "nascimento" ? "NASCIMENTO" : "ÓBITO"}
                    </span>
                  </div>
                </div>

                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                  <tbody>
                    {[
                      ["NUIC", resultado.nuic],
                      ["Nome completo", resultado.nome_completo],
                      resultado.tipo === "nascimento"
                        ? ["Data de nascimento", resultado.data_nascimento]
                        : ["Data de óbito", resultado.data_obito],
                      resultado.tipo === "nascimento"
                        ? ["Local de nascimento", resultado.local_nascimento]
                        : ["Local de óbito", resultado.local_obito],
                      ["Data de registo", resultado.aprovado_em],
                    ].map(([label, valor]) => (
                      <tr key={label} style={{ borderBottom: "1px solid #f0f0f0" }}>
                        <td style={{ padding: "10px 0", fontWeight: "bold", color: "#555", width: "45%" }}>{label}</td>
                        <td style={{ padding: "10px 0", color: "#222" }}>{valor}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                <p style={{ marginTop: "20px", fontSize: "12px", color: "#aaa", textAlign: "center" }}>
                  ✅ Registo verificado pela Conservatória do Registo Civil de Beira
                </p>
              </>
            ) : (
              <div style={{ textAlign: "center", padding: "20px" }}>
                <span style={{ fontSize: "50px" }}>❌</span>
                <h3 style={{ color: "#e74c3c", marginTop: "12px" }}>Nenhum registo encontrado</h3>
                <p style={{ color: "#888" }}>O NUIC introduzido não existe no sistema.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
