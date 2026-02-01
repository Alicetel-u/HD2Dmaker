using System;
using System.IO;
using System.Collections.Generic;
using System.Globalization;
using Yukar.Engine;
using Microsoft.Xna.Framework;

namespace Bakin
{
    /// <summary>
    /// HD2Dmaker Cinematic Director v2.3
    /// 会話表示対応版
    /// </summary>
    public class NewScript : BakinObject
    {
        private const string SCRIPT_PATH = @"c:\repos\HD2Dmaker\output\automation_script.txt";
        private const string LOG_PATH = @"c:\repos\HD2Dmaker\output\automation_log.txt";

        // スクリプト実行状態
        private bool isRunning = false;
        private List<string[]> commands = new List<string[]>();
        private int currentCommandIndex = 0;
        private float waitTimer = 0f;

        // 歩行状態
        private bool isWalking = false;
        private Vector3 walkTarget;
        private Vector3 walkDirection;
        private int currentDir = 1;
        private float moveSpeed = 4.0f;

        // 会話状態
        private bool isTalking = false;

        // 向き定義
        private const int DIR_UP = 0;
        private const int DIR_DOWN = 1;
        private const int DIR_RIGHT = 3;
        private const int DIR_LEFT = 2;

        [BakinFunction(Description = "HD2D Director v2.3 Talk")]
        public float Func(float attr)
        {
            if (isRunning) return 0;

            LoadScript();
            isRunning = true;
            currentCommandIndex = 0;
            waitTimer = 0f;
            isWalking = false;
            isTalking = false;

            Log("=== HD2D Director v2.3 (Talk support) ===");
            LogHeroPosition();

            return 1.0f;
        }

        private void LogHeroPosition()
        {
            var hero = mapScene?.hero;
            if (hero != null)
            {
                Vector3 pos = hero.getPosition();
                Log("Hero: X=" + pos.X.ToString("F2") + " Z=" + pos.Z.ToString("F2"));
            }
        }

        private void LoadScript()
        {
            commands.Clear();
            if (!File.Exists(SCRIPT_PATH)) return;

            string[] lines = File.ReadAllLines(SCRIPT_PATH);
            foreach (var line in lines)
            {
                string t = line.Trim();
                if (string.IsNullOrWhiteSpace(t) || t.StartsWith("#")) continue;
                commands.Add(t.Split('|'));
            }
            Log("Loaded " + commands.Count + " commands");
        }

        public override void Update()
        {
            if (!isRunning) return;

            float dt = 0.0166f;

            // 待機中
            if (waitTimer > 0)
            {
                waitTimer -= dt;
                return;
            }

            // 会話中（メッセージウィンドウが閉じるまで待つ）
            if (isTalking)
            {
                if (!IsMessageWindowActive())
                {
                    isTalking = false;
                    Log("Talk ended");
                }
                return;
            }

            // 歩行中
            if (isWalking)
            {
                UpdateWalk(dt);
                return;
            }

            // 次のコマンド実行
            if (currentCommandIndex < commands.Count)
            {
                ExecuteNextCommand();
            }
            else
            {
                isRunning = false;
                Log("=== Complete ===");
            }
        }

        private bool IsMessageWindowActive()
        {
            // メッセージウィンドウの状態チェックAPIが見つからないため、
            // isTalkingフラグはShowMessage呼び出し時にfalseのままにして
            // ユーザーがクリックで閉じるまで自動で待機する方式は使わない
            // 代わりに、WAITコマンドで待機時間を指定してもらう
            return false;
        }

        private void ShowMessage(string speaker, string message)
        {
            try
            {
                // 話者名をメッセージに含める
                string fullMessage = message;
                if (!string.IsNullOrEmpty(speaker))
                {
                    fullMessage = "【" + speaker + "】\n" + message;
                }

                Log("ShowMessage: " + fullMessage);

                if (mapScene != null)
                {
                    // ShowMessage(string message, int position, WindowTypes winType, Guid faceGraphic)
                    // position: 0=下, 1=中, 2=上 など（推測）
                    // WindowTypes: おそらく enum、0 = 通常
                    // Guid: 顔グラフィックのID（Guid.Empty = なし）

                    mapScene.ShowMessage(
                        fullMessage,
                        0,  // position (0 = 下)
                        MenuControllerBase.WindowTypes.DIALOGUE,  // ウィンドウタイプ
                        Guid.Empty  // 顔グラフィックなし
                    );

                    isTalking = true;
                    Log("ShowMessage called successfully");
                }
            }
            catch (Exception e)
            {
                Log("ShowMessage error: " + e.Message);
                // エラーの場合は待機せずに次へ進む
            }
        }

        private void UpdateWalk(float dt)
        {
            var hero = mapScene?.hero;
            if (hero == null) return;

            Vector3 pos = hero.getPosition();
            Vector3 diff = walkTarget - pos;
            diff.Y = 0;
            float dist = diff.Length();

            if (dist < 0.1f)
            {
                isWalking = false;
                hero.playMotion("wait");
                Log("Arrived");
                return;
            }

            hero.setDirection(currentDir, true, true);
            hero.playMotion("walk");

            float vx = walkDirection.X * moveSpeed * dt;
            float vz = walkDirection.Z * moveSpeed * dt;
            hero.Move(vx, vz, false, 0f);
        }

        private void SetupWalk(MapCharacter hero, string dirStr, int steps)
        {
            Vector3 pos = hero.getPosition();
            walkDirection = Vector3.Zero;

            switch (dirStr)
            {
                case "DOWN": case "D": case "S":
                    walkDirection = new Vector3(0, 0, 1);
                    currentDir = DIR_DOWN;
                    break;
                case "UP": case "U": case "W":
                    walkDirection = new Vector3(0, 0, -1);
                    currentDir = DIR_UP;
                    break;
                case "LEFT": case "L": case "A":
                    walkDirection = new Vector3(-1, 0, 0);
                    currentDir = DIR_LEFT;
                    break;
                case "RIGHT": case "R":
                    walkDirection = new Vector3(1, 0, 0);
                    currentDir = DIR_RIGHT;
                    break;
            }

            walkTarget = pos + walkDirection * steps;
            hero.setDirection(currentDir, true, true);
            Log("Walk " + dirStr + " x" + steps);
        }

        private int ParseDirection(string dirStr)
        {
            switch (dirStr.ToUpper())
            {
                case "DOWN": case "D": case "S": return DIR_DOWN;
                case "UP": case "U": case "W": return DIR_UP;
                case "LEFT": case "L": case "A": return DIR_LEFT;
                case "RIGHT": case "R": return DIR_RIGHT;
                default: return DIR_DOWN;
            }
        }

        private void ExecuteNextCommand()
        {
            string[] parts = commands[currentCommandIndex++];
            string cmd = parts[0].Trim().ToUpper();

            if (cmd != "LOG") Log(">> " + cmd);

            try
            {
                var hero = mapScene?.hero;

                switch (cmd)
                {
                    case "LOG":
                        Log(parts.Length > 1 ? parts[1] : "");
                        break;

                    case "WAIT":
                        waitTimer = float.Parse(parts[1], CultureInfo.InvariantCulture) / 1000f;
                        break;

                    case "WALK":
                        if (hero != null && parts.Length >= 3)
                        {
                            string d = parts[1].ToUpper();
                            int s = int.Parse(parts[2]);
                            if (s > 0)
                            {
                                isWalking = true;
                                SetupWalk(hero, d, s);
                            }
                        }
                        break;

                    case "FACE":
                        if (hero != null && parts.Length >= 2)
                        {
                            int dir = ParseDirection(parts[1]);
                            hero.setDirection(dir, true, true);
                            currentDir = dir;
                        }
                        break;

                    case "DIR":
                        if (hero != null && parts.Length >= 2)
                        {
                            int dir = int.Parse(parts[1]);
                            hero.setDirection(dir, true, true);
                            currentDir = dir;
                        }
                        break;

                    case "MOTION":
                        if (hero != null && parts.Length >= 2)
                        {
                            hero.playMotion(parts[1]);
                        }
                        break;

                    case "SPEED":
                        if (parts.Length >= 2)
                        {
                            moveSpeed = float.Parse(parts[1], CultureInfo.InvariantCulture);
                            Log("Speed: " + moveSpeed);
                        }
                        break;

                    // 会話コマンド
                    case "SAY":
                    case "TALK":
                        if (parts.Length >= 3)
                        {
                            string speaker = parts[1];
                            string message = parts[2];
                            ShowMessage(speaker, message);
                        }
                        else if (parts.Length >= 2)
                        {
                            ShowMessage("", parts[1]);
                        }
                        break;

                    case "MSG":
                    case "MESSAGE":
                        if (parts.Length >= 2)
                        {
                            ShowMessage("", parts[1]);
                        }
                        break;

                    default:
                        Log("Unknown: " + cmd);
                        break;
                }
            }
            catch (Exception e)
            {
                Log("Error: " + e.Message);
            }
        }

        private void Log(string msg)
        {
            try
            {
                File.AppendAllText(LOG_PATH, "[" + DateTime.Now.ToString("HH:mm:ss.fff") + "] " + msg + "\n");
            }
            catch { }
        }
    }
}
