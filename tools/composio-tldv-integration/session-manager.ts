/**
 * Session Manager - Persistência de Sessões Autorizadas
 * Salva as sessões autorizadas localmente para reutilização
 */

import * as fs from "fs";
import * as path from "path";

interface SavedSession {
  sessionId: string;
  externalUserId: string;
  connectedAccountId?: string;
  connectedAt: string;
  expiresAt?: string;
  authorizedApps: string[];
}

export class SessionManager {
  private sessionsDir: string;
  private sessionsFile: string;

  constructor(sessionsDir: string = ".composio-sessions") {
    this.sessionsDir = sessionsDir;
    this.sessionsFile = path.join(sessionsDir, "sessions.json");

    // Criar diretório se não existir
    if (!fs.existsSync(sessionsDir)) {
      fs.mkdirSync(sessionsDir, { recursive: true });
    }
  }

  /**
   * Salvar sessão autorizada
   */
  saveSession(session: SavedSession): void {
    try {
      const sessions = this.getAllSessions();

      // Atualizar ou adicionar sessão
      const index = sessions.findIndex((s) => s.externalUserId === session.externalUserId);
      if (index >= 0) {
        sessions[index] = session;
      } else {
        sessions.push(session);
      }

      // Salvar em arquivo
      fs.writeFileSync(this.sessionsFile, JSON.stringify(sessions, null, 2));
      console.log(`✅ Sessão salva para ${session.externalUserId}`);
    } catch (error) {
      console.error("❌ Erro ao salvar sessão:", error);
      throw error;
    }
  }

  /**
   * Carregar sessão autorizada
   */
  loadSession(externalUserId: string): SavedSession | null {
    try {
      const sessions = this.getAllSessions();
      const session = sessions.find((s) => s.externalUserId === externalUserId);

      if (session) {
        console.log(`✅ Sessão carregada para ${externalUserId}`);
        return session;
      }

      return null;
    } catch (error) {
      console.error("❌ Erro ao carregar sessão:", error);
      return null;
    }
  }

  /**
   Obter todas as sessões salvas
   */
  getAllSessions(): SavedSession[] {
    try {
      if (!fs.existsSync(this.sessionsFile)) {
        return [];
      }

      const data = fs.readFileSync(this.sessionsFile, "utf-8");
      return JSON.parse(data) || [];
    } catch (error) {
      console.error("❌ Erro ao ler sessões:", error);
      return [];
    }
  }

  /**
   * Deletar sessão
   */
  deleteSession(externalUserId: string): void {
    try {
      const sessions = this.getAllSessions();
      const filtered = sessions.filter((s) => s.externalUserId !== externalUserId);

      if (filtered.length < sessions.length) {
        fs.writeFileSync(this.sessionsFile, JSON.stringify(filtered, null, 2));
        console.log(`✅ Sessão deletada para ${externalUserId}`);
      }
    } catch (error) {
      console.error("❌ Erro ao deletar sessão:", error);
      throw error;
    }
  }

  /**
   * Verificar se sessão existe e é válida
   */
  isSessionValid(externalUserId: string): boolean {
    const session = this.loadSession(externalUserId);
    if (!session) return false;

    // Verificar expiração se houver
    if (session.expiresAt) {
      const expiresAt = new Date(session.expiresAt);
      if (new Date() > expiresAt) {
        console.log(`⚠️  Sessão expirada para ${externalUserId}`);
        this.deleteSession(externalUserId);
        return false;
      }
    }

    return true;
  }

  /**
   * Listar todas as sessões salvas
   */
  listSessions(): void {
    const sessions = this.getAllSessions();

    if (sessions.length === 0) {
      console.log("📭 Nenhuma sessão salva");
      return;
    }

    console.log(`\n📋 Sessões Salvas (${sessions.length}):\n`);
    sessions.forEach((session, index) => {
      console.log(`${index + 1}. ${session.externalUserId}`);
      console.log(`   Session ID: ${session.sessionId}`);
      console.log(`   Conectado em: ${new Date(session.connectedAt).toLocaleString("pt-BR")}`);
      console.log(`   Apps autorizados: ${session.authorizedApps.join(", ")}`);
      console.log();
    });
  }

  /**
   * Limpar todas as sessões
   */
  clearAllSessions(): void {
    try {
      if (fs.existsSync(this.sessionsFile)) {
        fs.unlinkSync(this.sessionsFile);
        console.log("✅ Todas as sessões foram limpas");
      }
    } catch (error) {
      console.error("❌ Erro ao limpar sessões:", error);
      throw error;
    }
  }

  /**
   * Adicionar app autorizado a uma sessão
   */
  addAuthorizedApp(externalUserId: string, app: string): void {
    const session = this.loadSession(externalUserId);
    if (session) {
      if (!session.authorizedApps.includes(app)) {
        session.authorizedApps.push(app);
        this.saveSession(session);
        console.log(`✅ App '${app}' adicionado aos autorizados`);
      }
    }
  }
}

export default SessionManager;
