import React, { useState } from "react";
import {
  Settings,
  Volume2,
  VolumeX,
  Bell,
  BellOff,
} from "lucide-react";

interface ChatSettingsProps {
  isOpen: boolean;
  onClose: () => void;
  onSettingsChange: (settings: ChatSettings) => void;
}

export interface ChatSettings {
  soundEnabled: boolean;
  notificationsEnabled: boolean;
  theme: "light" | "dark" | "auto";
  fontSize: "small" | "medium" | "large";
  autoScroll: boolean;
  showTypingIndicator: boolean;
}

const defaultSettings: ChatSettings = {
  soundEnabled: true,
  notificationsEnabled: true,
  theme: "auto",
  fontSize: "medium",
  autoScroll: true,
  showTypingIndicator: true,
};

export const ChatSettingsPanel: React.FC<ChatSettingsProps> = ({
  isOpen,
  onClose,
  onSettingsChange,
}) => {
  const [settings, setSettings] = useState<ChatSettings>(() => {
    const saved = localStorage.getItem("chatSettings");
    return saved ? JSON.parse(saved) : defaultSettings;
  });

  const updateSetting = <K extends keyof ChatSettings>(
    key: K,
    value: ChatSettings[K]
  ) => {
    const newSettings = { ...settings, [key]: value };
    setSettings(newSettings);
    localStorage.setItem("chatSettings", JSON.stringify(newSettings));
    onSettingsChange(newSettings);
  };

  if (!isOpen) return null;

  return (
    <div className="absolute top-0 left-0 right-0 bottom-0 bg-[#f5f5f5] z-50 flex flex-col font-sans">
      {/* Header */}
      <div className="bg-[#002855] text-white p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Settings className="w-5 h-5" />
          <h2 className="font-medium">Configuración del Chat</h2>
        </div>
        <button
          onClick={onClose}
          className="p-1 hover:bg-[#001F3F] rounded transition-colors"
        >
          ×
        </button>
      </div>

      {/* Settings Content */}
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-6">
          {/* Audio Settings */}
          <div>
            <h3 className="font-medium text-[#002855] mb-3">Audio</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {settings.soundEnabled ? (
                    <Volume2 className="w-4 h-4 text-[#FFD100]" />
                  ) : (
                    <VolumeX className="w-4 h-4 text-gray-400" />
                  )}
                  <span className="text-sm">Sonidos</span>
                </div>
                <button
                  onClick={() =>
                    updateSetting("soundEnabled", !settings.soundEnabled)
                  }
                  className={`w-10 h-6 rounded-full transition-colors ${
                    settings.soundEnabled ? "bg-[#FFD100]" : "bg-gray-300"
                  }`}
                >
                  <div
                    className={`w-4 h-4 bg-white rounded-full transition-transform ${
                      settings.soundEnabled ? "translate-x-5" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {settings.notificationsEnabled ? (
                    <Bell className="w-4 h-4 text-[#FFD100]" />
                  ) : (
                    <BellOff className="w-4 h-4 text-gray-400" />
                  )}
                  <span className="text-sm">Notificaciones</span>
                </div>
                <button
                  onClick={() =>
                    updateSetting(
                      "notificationsEnabled",
                      !settings.notificationsEnabled
                    )
                  }
                  className={`w-10 h-6 rounded-full transition-colors ${
                    settings.notificationsEnabled
                      ? "bg-[#FFD100]"
                      : "bg-gray-300"
                  }`}
                >
                  <div
                    className={`w-4 h-4 bg-white rounded-full transition-transform ${
                      settings.notificationsEnabled
                        ? "translate-x-5"
                        : "translate-x-1"
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>

          {/* Appearance Settings */}
          <div>
            <h3 className="font-medium text-[#002855] mb-3">Apariencia</h3>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tema
                </label>
                <div className="flex space-x-2">
                  {(["light", "dark"] as const).map((theme) => (
                    <button
                      key={theme}
                      onClick={() => updateSetting("theme", theme)}
                      className={`px-3 py-2 text-xs rounded-md border ${
                        settings.theme === theme
                          ? "bg-[#003f7f] border-[#001F3F] text-white"
                          : "bg-white border-gray-300 text-gray-700"
                      }`}
                    >
                      {theme === "light" ? "Claro" : "Oscuro"}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tamaño de fuente
                </label>
                <div className="flex space-x-2">
                  {(["small", "medium", "large"] as const).map((size) => (
                    <button
                      key={size}
                      onClick={() => updateSetting("fontSize", size)}
                      className={`px-3 py-2 text-xs rounded-md border ${
                        settings.fontSize === size
                          ? "bg-[#003f7f] border-[#001F3F] text-white"
                          : "bg-white border-gray-300 text-gray-700"
                      }`}
                    >
                      {size === "small"
                        ? "Pequeño"
                        : size === "medium"
                        ? "Mediano"
                        : "Grande"}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Behavior Settings */}
          <div>
            <h3 className="font-medium text-[#002855] mb-3">Comportamiento</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm">Desplazamiento automático</span>
                <button
                  onClick={() =>
                    updateSetting("autoScroll", !settings.autoScroll)
                  }
                  className={`w-10 h-6 rounded-full transition-colors ${
                    settings.autoScroll ? "bg-[#FFD100]" : "bg-gray-300"
                  }`}
                >
                  <div
                    className={`w-4 h-4 bg-white rounded-full transition-transform ${
                      settings.autoScroll ? "translate-x-5" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm">Mostrar indicador de escritura</span>
                <button
                  onClick={() =>
                    updateSetting(
                      "showTypingIndicator",
                      !settings.showTypingIndicator
                    )
                  }
                  className={`w-10 h-6 rounded-full transition-colors ${
                    settings.showTypingIndicator
                      ? "bg-[#FFD100]"
                      : "bg-gray-300"
                  }`}
                >
                  <div
                    className={`w-4 h-4 bg-white rounded-full transition-transform ${
                      settings.showTypingIndicator
                        ? "translate-x-5"
                        : "translate-x-1"
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t p-4 bg-[#002855] text-white text-xs flex justify-between items-center">
        <span>InfoBot v2.0 - GRUPO INFOTEC</span>
        <button
          onClick={() => {
            setSettings(defaultSettings);
            localStorage.removeItem("chatSettings");
            onSettingsChange(defaultSettings);
          }}
          className="underline hover:text-[#FFD100] transition-colors"
        >
          Restaurar valores predeterminados
        </button>
      </div>
    </div>
  );
};
