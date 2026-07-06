export interface Judge {
  id: string;
  name: string;
  category: string;
  summary?: string;
  description?: string;
  tags?: string[];
  scoreRange?: string;
  /** Full runnable GGX module source. */
  code: string;
  /** Prompt template text. */
  prompt: string;
}
