import React, { useState } from "react";
import {
  Settings,
  Volume2,
  VolumeX,
  Bell,
  BellOff,
  Palette,
  Monitor,
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
    <div className="absolute top-0 left-0 right-0 bottom-0 bg-white z-50 flex flex-col">
      {/* Header */}
      <div className="bg-[var(--infotec-orange)] text-white p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Settings className="w-5 h-5" />
          <h2 className="font-medium">Configuración del Chat</h2>
        </div>
        <button
          onClick={onClose}
          className="p-1 hover:bg-[var(--infotec-orange-dark)] rounded transition-colors"
        >
          ×
        </button>
      </div>

      {/* Settings Content */}
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-6">
          {/* Audio Settings */}
          <div>
            <h3 className="font-medium text-gray-800 mb-3">Audio</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {settings.soundEnabled ? (
                    <Volume2 className="w-4 h-4 text-[var(--infotec-orange)]" />
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
                    settings.soundEnabled
                      ? "bg-[var(--infotec-orange)]"
                      : "bg-gray-300"
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
                    <Bell className="w-4 h-4 text-[var(--infotec-orange)]" />
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
                      ? "bg-[var(--infotec-orange)]"
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
            <h3 className="font-medium text-gray-800 mb-3">Apariencia</h3>
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
                          ? "bg-orange-500 border-orange-600 text-white"
                          : "bg-gray-50 border-gray-300 text-gray-700"
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
                          ? "bg-orange-500 border-orange-600 text-white"
                          : "bg-gray-50 border-gray-300 text-gray-700"
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
            <h3 className="font-medium text-gray-800 mb-3">Comportamiento</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm">Desplazamiento automático</span>
                <button
                  onClick={() =>
                    updateSetting("autoScroll", !settings.autoScroll)
                  }
                  className={`w-10 h-6 rounded-full transition-colors ${
                    settings.autoScroll
                      ? "bg-[var(--infotec-orange)]"
                      : "bg-gray-300"
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
                      ? "bg-[var(--infotec-orange)]"
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
      <div className="border-t p-4">
        <div className="flex justify-between items-center">
          <span className="text-xs text-gray-500">
            InfoBot v2.0 - GRUPO INFOTEC
          </span>
          <button
            onClick={() => {
              setSettings(defaultSettings);
              localStorage.removeItem("chatSettings");
              onSettingsChange(defaultSettings);
            }}
            className="text-xs text-gray-500 hover:text-gray-700 underline"
          >
            Restaurar valores predeterminados
          </button>
        </div>
      </div>
    </div>
  );
};
