export interface LoginResponse {
  id: string,
  email: string,
  username: string,
  public_key: string,
  private_key: string,
  creation_date: string,
  email_verification_date: string,
}

export interface UserEntity {
  id: string,
  email: string
  username: string
  publicKey: string,
  privateKey: string,
}
